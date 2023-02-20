# pot_ignored_scopes_gen

Tool to generate pot ignored scopes for given IR.

Usage:
```
python ir_name_map_util.py pattern <xml IR path> <path to pattern> <path to output json>
```

Config description:
```
{
 <Pattern name>:
  {
   "pattern": [[<Node type 0>, <Node type 1>, ..,], ...],
   "idx": <Node index to take from mathed graph>,
   "num_matches": <Reference mathes number>,
   "idxs_selection": [<Indexes of mathes to take. If empty - takes all mathes>]
  }, ...
}
```
