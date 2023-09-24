# DATA PLATFORM PROJECT TEMPLATE

## Sprint Sep25 to Sep29
- registry flow
```text
user --> api (to registry)
action: 
    update (add) kafka topic
    update (add) database manager consume config
    update (add) database (or table)
```
- data consume flow
```text
device --> kafka <--> database manager --> preprocess (optional) --> save to database
```
- dev `api` with:
```text
fastAPI
pydandic BaseModel
pykafka
```
- dev `database manager` `structure` `some sample` `query`
```text
database control by python API of database
```
- study on `protocols` `middleware` `security (optional)`
- test
```text
full flow bug
data/database syncing
```