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

import logging

from ncclient.xml_ import to_xml, to_ele
from napalm.base.helpers import convert
from .util import _find_txt, NSMAP

#
# Netconf filters to retrieve only required attributes
#

NEIGHBOR_CONF = """
<neighbor>
    <ip-address>{neighbor_address}</ip-address>
    <peer-as/>
    <local-address/>
    <multihop/>
    <multipath-eligible/>
    <asn-4-byte/>
    <keepalive/>
    <local-as>
        <as-number/>
        <prepend-global-as/>
    </local-as>
    <remove-private>
        <limited/>
    </remove-private>
    <import>
        <policy/>
    </import>
    <export>
        <policy/>
    </export>
    <hold-time>
        <seconds/>
        <minimum-hold-time/>
    </hold-time>
</neighbor>
"""

NEIGHBOR_STATS = """
<bgp>
<neighbor>
<ip-address>{neighbor_address}</ip-address>
<statistics>
    <session-state/>
    <local-port/>
    <peer-identifier/>
    <peer-port/>
    <operational-local-address/>
    <operational-remote-address/>
    <last-state/>
    <last-event/>
    <keep-alive-interval/>
    <hold-time-interval/>
    <number-of-update-flaps/>
    <received>
        <messages/>
        <updates/>
    </received>
    <sent>
        <messages/>
        <updates/>
        <queues/>
    </sent>
    <family-prefix>
        <ipv4>
            <active/>
            <received/>
            <suppressed/>
            <rejected/>
            <sent/>
        </ipv4>
        <ipv6>
            <active/>
            <received/>
            <suppressed/>
            <rejected/>
            <sent/>
        </ipv6>
    </family-prefix>
</statistics>
</neighbor>
</bgp>
"""

GET_BGP_NEIGHBORS_DETAILS = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
            <router>
                <router-name/>
                <autonomous-system/>
                <bgp>
                """+NEIGHBOR_CONF+"""
                </bgp>
            </router>
            <service>
                <vprn>
                    <service-name/>
                    <autonomous-system/>
                    <bgp>
                    """+NEIGHBOR_CONF+"""
                    </bgp>
                </vprn>
            </service>
        </configure>
        <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
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

def get_bgp_neighbors_detail(conn,neighbor_address=""):
  data = to_ele(
      conn.get(
          filter=GET_BGP_NEIGHBORS_DETAILS.format(
              neighbor_address=neighbor_address
          ),
          with_defaults="report-all",
      ).data_xml
  )
  if log.isEnabledFor(logging.DEBUG):
    log.debug(to_xml(data, pretty_print=True))
  result = {}
  for n in data.xpath("//configure_ns:neighbor",namespaces=NSMAP):
    name = _find_txt(n, "../../configure_ns:service-name") or "global"
    local_as = convert(int, _find_txt( n, "../../configure_ns:autonomous-system" ))

    ip_address = _find_txt( n, "configure_ns:ip-address" )
    stats = data.xpath( f"//state_ns:ip-address[ text()='{ip_address}']/..", namespaces=NSMAP)

    def conf_int(attr: str,default=0):
      return convert( int, _find_txt(n,f"configure_ns:{attr}")) or default

    def state_int(attr: str):
      return convert( int, _find_txt(stats[0],f"state_ns:statistics/state_ns:{attr}"))

    def conf_str(attr: str):
      return _find_txt(n,f"configure_ns:{attr}")

    def conf_bool(attr:str):
      return conf_str(attr).lower() == "true"

    def conf_list(attr:str):
      policies = [ele.text for ele in n.xpath(attr,namespaces=NSMAP)]
      return ",".join(policies)

    def state_str(attr: str):
      return _find_txt(stats[0],f"state_ns:statistics/state_ns:{attr}")

    session_state = state_str('session-state')

    count = {}
    for attr in ['active','suppressed','rejected','sent','received']:
      count[attr] = {}
      for af in ('ipv4','ipv6'):
        count[attr][af] = convert(
            int,
            _find_txt(
                stats[0],
                f"state_ns:statistics/state_ns:family-prefix/state_ns:{af}/state_ns:{attr}"
            )
        )
      count[attr]['total'] = count[attr]['ipv4'] + count[attr]['ipv6']

    peer = {
      'up': session_state.lower()=="established",
      'local_as': local_as,
      'remote_as': conf_int('peer-as'),
      'router_id': state_str('peer-identifier'),
      'local_address': state_str('operational-local-address'),
      'routing_table': name,
      'local_address_configured': conf_str('local-address') != "",
      'local_port': state_int('local-port'),
      'remote_address': ip_address,
      'remote_port': state_int('peer-port'),
      'multihop': conf_int('multihop') > 0,
      'multipath': conf_str('multipath-eligible') != "false",
      'remove_private_as': conf_bool('remove-private/configure_ns:limited'),
      'import_policy': conf_list('import/configure_ns:policy'),
      'export_policy': conf_list('export/configure_ns:policy'),
      'input_messages': state_int('received/state_ns:messages'),
      'output_messages': state_int('sent/state_ns:messages'),
      'input_updates': state_int('received/state_ns:updates'),
      'output_updates': state_int('sent/state_ns:updates'),
      'messages_queued_out': state_int('sent/state_ns:queues'),
      'connection_state': session_state,
      'previous_connection_state': state_str('last-state'),
      'last_event': state_str('last-event'),
      'suppress_4byte_as': conf_str('asn-4-byte') == 'false',
      'local_as_prepend': conf_bool('local-as/configure_ns:prepend-global-as'),
      'holdtime': state_int('hold-time-interval'),
      'configured_holdtime': conf_int('hold-time/configure_ns:seconds'),
      'keepalive': state_int('keep-alive-interval'),
      'configured_keepalive': conf_int('keepalive'),
      'active_prefix_count': count['active']['total'],
      'received_prefix_count': count['received']['total'],
      'accepted_prefix_count': count['received']['total'] - count['rejected']['total'],
      'suppressed_prefix_count': count['suppressed']['total'],
      'advertised_prefix_count': count['sent']['total'],
      'flap_count': state_int('number-of-update-flaps')
    }

    if name not in result:
      result[name] = {}
    if peer['remote_as'] not in result[name]:
      result[name][ peer['remote_as'] ] = []
    result[name][ peer['remote_as'] ].append(peer)

  return result
