#!/usr/bin/env python

# -*- coding: utf-8 -*-
# © 2022 Nokia
# Licensed under the Apache License 2.0 License
# SPDX-License-Identifier: Apache-2.0

#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import logging, datetime

from ncclient.xml_ import to_xml, to_ele
from napalm.base.helpers import convert

from .util import _find_txt, NSMAP

#
# Netconf filters to retrieve only required attributes
#
NEIGHBOR_CONF = """
<autonomous-system/>
<bgp>
    <neighbor>
        <ip-address/>
        <admin-state/>
        <description/>
        <peer-as/>
        <local-as>
            <as-number/>
        </local-as>
    </neighbor>
</bgp>
"""

NEIGHBOR_STATS = """
<oper-router-id/>
<bgp>
    <neighbor>
        <ip-address/>
        <statistics>
            <peer-identifier/>
            <session-state/>
            <last-established-time/>
            <family-prefix>
                <ipv4>
                    <received/>
                    <active/>
                    <sent/>
                </ipv4>
                <ipv6>
                    <received/>
                    <active/>
                    <sent/>
                </ipv6>
            </family-prefix>
        </statistics>
    </neighbor>
</bgp>
"""

GET_BGP_NEIGHBORS = """
    <filter>
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
            <router-name/>
            """+NEIGHBOR_CONF+"""
            </router>
            <service>
                <vprn>
                <service-name/>
            """+NEIGHBOR_CONF+"""
                </vprn>
            </service>
        </configure>
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
            <system>
                <current-time/>
            </system>
            <router>
                """+NEIGHBOR_STATS+"""
            </router>
            <service>
                <vprn>
                """+NEIGHBOR_STATS+"""
                </vprn>
            </service>
        </state>
    </filter>
"""

log = logging.getLogger(__file__)

def get_bgp_neighbors(conn):
  data = to_ele(
      conn.get(
          filter=GET_BGP_NEIGHBORS,
          with_defaults="report-all",
      ).data_xml
  )
  if log.isEnabledFor(logging.DEBUG):
    log.debug(to_xml(data, pretty_print=True))

  current_time_str = _find_txt(data,'//state_ns:system/state_ns:current-time')

  # List all VRFs and the operational local router ID
  result = {
    'global': {
      'router_id': _find_txt(data,"//state_ns:router/state_ns:oper-router-id"),
      'peers': {}
    }
  }
  for vprn in data.xpath("//state_ns:service/state_ns:vprn",namespaces=NSMAP):
    name = _find_txt(vprn, "state_ns:service-name")
    router_id = _find_txt(vprn, "state_ns:oper-router-id")
    result[ name ] = { 'router_id': router_id, 'peers': {} }

  for n in data.xpath("//configure_ns:neighbor",namespaces=NSMAP):
    name = _find_txt(n, "../../configure_ns:service-name") or "global"
    local_as = convert(int, _find_txt( n, "../../configure_ns:autonomous-system" ))

    ip_address = _find_txt( n, "configure_ns:ip-address" )
    stats = data.xpath( f"//state_ns:ip-address[ text()='{ip_address}']/..", namespaces=NSMAP)

    def conf_int(attr: str,default=0):
      return convert( int, _find_txt(n,f"configure_ns:{attr}")) or default

    def conf_str(attr: str):
      return _find_txt(n,f"configure_ns:{attr}")

    def state_str(attr: str):
      return _find_txt(stats[0],f"state_ns:statistics/state_ns:{attr}")

    def to_timestamp(time:str):
      if time:
        # Remove 'Z' timezone
        return datetime.datetime.strptime(time[:-1], "%Y-%m-%dT%H:%M:%S.%f").timestamp()
      return 0

    session_state = state_str('session-state')
    router_id = _find_txt( data, f"//state_ns:ip-address[text()='{ip_address}']/../../../state_ns:oper-router-id" )

    count = {}
    for attr in ['received','active','sent']:
      count[attr] = {}
      for af in ('ipv4','ipv6'):
        count[attr][af] = convert(
            int,
            _find_txt(
                stats[0],
                f"state_ns:statistics/state_ns:family-prefix/state_ns:{af}/state_ns:{attr}"
            )
        )

    last_established_time = to_timestamp(state_str('last-established-time'))
    uptime = to_timestamp(current_time_str) - last_established_time

    peer = {
      'local_as': local_as,
      'remote_as': conf_int('peer-as'),
      'remote_id': state_str('peer-identifier'),
      'is_up': session_state.lower()=="established",
      'is_enabled': conf_str('admin-state') == "enable",
      'description': conf_str('description'),
      'uptime': convert(int,uptime), # Current or time since down if is_up=False
      'address_family': {
        'ipv4': {
         'received_prefixes': count['received']['ipv4'],
         'accepted_prefixes': count['active']['ipv4'],
         'sent_prefixes': count['sent']['ipv4'],
        },
        'ipv6': {
         'received_prefixes': count['received']['ipv6'],
         'accepted_prefixes': count['active']['ipv6'],
         'sent_prefixes': count['sent']['ipv6'],
        }
      }
    }
    result[name]['peers'][ip_address] = peer

  return result
