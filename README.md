# pot_ignored_scopes_gen

Tool to generate pot ignored scopes for given IR.

***WARNING:***
Skript doesn't use any informantion about edges, so it assumes nodes in IR are in topological order 

Usage:
```
python ir_name_map_util.py pattern <xml IR path> <path to pattern> <path to output json>
```

***NB***:
Please check that reference amount of mathes equal to actual amount of mathces

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
