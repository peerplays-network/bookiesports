#!/usr/bin/env python3

import yaml
from jsonschema import validate

defs = yaml.load(open("schema-definitions.yaml", "r"))

schema_sport = yaml.load(open("schema-sport.yaml", "r"))
schema_eventgroup = yaml.load(open("schema-eventgroup.yaml", "r"))
schema_bettingmarketgroup = yaml.load(open("schema-bettingmarketgroup.yaml", "r"))
schema_participants = yaml.load(open("schema-participants.yaml", "r"))
schema_rules = yaml.load(open("schema-rules.yaml", "r"))

schema_sport.update(defs)
schema_eventgroup.update(defs)
schema_bettingmarketgroup.update(defs)
schema_participants.update(defs)
schema_rules.update(defs)

sport = yaml.load(open("AmericanFootball/index.yaml", "r"))
eventgroup = yaml.load(open("AmericanFootball/NFL#PreSeas/index.yaml", "r"))
bmg = yaml.load(open("AmericanFootball/bettingmarketgroups/NFL_HCP_2017-18_1.yaml", "r"))
parts = yaml.load(open("AmericanFootball/participants/NFL_Teams_2017-18.yaml", "r"))
rules = yaml.load(open("AmericanFootball/rules/R_NFL_MO_1.yaml", "r"))


validate(sport, schema_sport)
validate(eventgroup, schema_eventgroup)
validate(bmg, schema_bettingmarketgroup)
validate(parts, schema_participants)
validate(rules, schema_rules)
