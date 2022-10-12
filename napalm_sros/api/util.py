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

import logging, traceback

NSMAP = {
 "state_ns": "urn:nokia.com:sros:ns:yang:sr:state",
 "configure_ns": "urn:nokia.com:sros:ns:yang:sr:conf",
}

def _find_txt(xml_tree, path, default="", namespaces=NSMAP):
    """
    Extracts the text value from an XML tree, using XPath.
    In case of error, will return a default value.

    :param xml_tree:   the XML Tree object. Assumed is <type 'lxml.etree._Element'>.
    :param path:       XPath to be applied, in order to extract the desired data.
    :param default:    Value to be returned in case of error.
    :param namespaces: prefix-namespace mappings to process XPath
    :return: a str value.
    """
    value = ""
    try:
        xpath_applied = xml_tree.xpath(
            path, namespaces=namespaces
        )  # will consider the first match only
        xpath_length = len(xpath_applied)  # get a count of items in XML tree
        if xpath_length and xpath_applied[0] is not None:
            xpath_result = xpath_applied[0]
            if isinstance(xpath_result, type(xml_tree)):
                if xpath_result.text is not None:
                    value = xpath_result.text.strip()
            else:
                value = xpath_result
        else:
            if xpath_applied == "":
                logging.error(
                    "Unable to find the specified-text-element/XML path: %s in  \
                        the XML tree provided. Total Items in XML tree: %d "
                    % (path, xpath_length)
                )
    except Exception as e:  # in case of any exception, returns default
        print("Error while finding text in xml: {}".format(e))
        logging.error("Error while finding text in xml: %s" % traceback.format_exc())
        value = default
    return str(value)
