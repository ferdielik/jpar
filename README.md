# Pretty Json Parser
This tool helps to show the json data collected from different sources in a single format.

## Install
```
pip install jpar
```

## Result
### Inputs
```
{"name":"Sherlock","surname":"Holmes","age":87} // source 1
{"firstname":"Steve","lastsurname":"Jobs","userAge":111,"useless":"dummy"} // source 2
{"f":"Albert","l":"Einstein","a":37} // source 3
```

### Output
```
[
  {
    "age": 87.0,
    "name": "Sherlock",
    "surname": "Holmes"
  },
  {
    "name": "Steve",
    "surname": "Jobs"
  },
  {
    "age": 37.0,
    "name": "Albert",
    "surname": "Einstein"
  }
]
```

## Usage
Only you have to define format files, for above example format files
```
{
  "age": ##age|N##,
  "name": ##name|S##,
  "surname": ##surname|S##
}
---
{
  "firstname": ##name|S##,
  "lastsurname": ##surname|S##,
  "userAge": ##age|N##
}
---
{
  "a": ##age|N##,
  "f": ##name|S##,
  "l": ##surname|S##
}
```

For the results
```
from jpar.parser import jpar_with_file

results = []
results.append(jpar_with_file('data/source1.json', 'format/source1_format.json'))
results.append(jpar_with_file('data/source2.json', 'format/source2_format.json'))
results.append(jpar_with_file('data/source3.json', 'format/source3_format.json'))
print(results) # it give you above output

```