db.auth('root', 'pws')

db = db.getSiblingDB('db_name')

db.createUser({ user:"username", 
                pwd:"password", 
                roles:[ { role:"readWrite", 
                          db:"db_name" 
                        } ], 
                mechanisms:[ "SCRAM-SHA-1"] 
              })
              
db.createCollection('collection_name')

