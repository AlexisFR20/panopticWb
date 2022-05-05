class AguilasRouter(object): 
    def db_for_read(self, model, **hints):
        "Point all operations on aguilas models to 'aguilas'"
        if model._meta.db_table  == 'CIAA_R1':
            return 'aguilas'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on chinook models to 'chinookdb'"
        if model._meta.db_table == 'CIAA_R1':
            return 'aguilas'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in chinook app"
        if obj1._meta.db_table == 'CIAA_R1' and obj2._meta.db_table == 'CIAA_R1':
            return True
        # Allow if neither is chinook app
        elif 'aguilas' not in [obj1._meta.db_table, obj2._meta.db_table]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'CIAA_R1' or model._meta.db_table == "CIAA_R1":
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True