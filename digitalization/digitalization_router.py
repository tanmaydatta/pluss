class Digitalization(object): 
    def db_for_read(self, model, **hints):
        "Point all operations on pluss models to 'plussdb'"
        if model._meta.app_label == 'digitalization':
            return 'pluss'
        return 'default'

    def db_for_write(self, model, **hints):
        "Point all operations on pluss models to 'plussdb'"
        if model._meta.app_label == 'digitalization':
            return 'pluss'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in pluss app"
        if obj1._meta.app_label == 'digitalization' and obj2._meta.app_label == 'digitalization':
            return True
        # Allow if neither is pluss app
        elif 'digitalization' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True