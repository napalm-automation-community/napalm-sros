Value ServId (\S+)
Value MAC (\S+)
Value Source_Identifier (\S+)
Value Source_Identifier__ (\S+)
Value Type (\S+)
Value Type__ (\S+)
Value Age (\d+)
Value Last_Change (\S+\s+\S+)
Value Transport_Tnl_Id (\S+)


Start
  ^-{5,} -> Entries

Entries
  ^\S+\s+\S+\s+\S+\s+\S+\s+\S+ -> Continue.Record
  ^${ServId}\s+${MAC}\s+${Source_Identifier}\s+${Type}\s+${Last_Change}
  ^\s{53}${Type__}
  ^\s{29}${Source_Identifier__}(\s+${Type__})?
  ^\s{11}${Transport_Tnl_Id}
  ^-{5,} -> EOF
