#!/usr/bin/env python

class RuleError(Exception):
    pass

class Schema(object):
    def __init__(self):

        self.rules = {}

    def get_rule(self, name):
        return self.rules[name]

    def create_rule(self, name, type, length, required=False, codes=False, 
    	            regex=False):
        
        if name not in self.rules.keys():
            self.rules[name] = {'type': type,
                                'length': length,
                                'required': required,
                                'codes': codes,
                                'regex': regex}
            
            return "New rule created: %s" % (self.rules[name])

        else:
            raise RuleError('rule for %s already exists' % (name)) 

    def update_rule(self, name, length, type, required=False, codes=False,
                    regex=False):
        
        if self.rules[name]:
            self.rules[name] = {'length': length,
                                'type': type,
                                'required': required,
                                'codes': codes,
                                'regex': regex}

            return "Existing rule updated: %s" % (self.rules[name])

        else:
            raise RuleError('rule for %s does not exist' % (name))

    def delete_rule(self, name):
        
        if self.rules[name]:
            self.rules.pop(name)

            return "Existing rule deleted: %s" % (name)
        
        else:
            raise RuleError('rule for %s does not exist' % (name))


# if __name__ == "__main__":

#     rules = {}
#     test_schema = Schema()
#     test_schema.create_rule(name='test', length=4, type=str)

#     print test_schema.rules
