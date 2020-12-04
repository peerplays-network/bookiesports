# A particular Sport

Now that we are within a particular sport, we can give more information
about it. Most importantly, each Sport has an internationalized name
and a blockchain id associated with it.

```
   name:
       en: American Football
       de: Amerikanisches Football 
   id: 1.xxx.yyy
```

The internationalized attribute `name`, here, distinguishes between `en`
and `de` as languages. Others may be added freely.

# Event groups

Every event group needs to be listed in the `index.yaml` file for
further processing.

# Betting Market Groups

Betting market groups that can (and are) used within events of this
sport are all listed and defined in the sub folder `bettingmarketgroups/`.
If an event wants to make use of a particular betting market group type,
it needs to be defined here.

# Participants

A full list of participants for this sport is provided as file in the
`participants/` sub directory. Every year, this folder will at least
grow by one file.

# Rules and Gradings

The rules (human readable) and gradings (machine readable) are defined
in `rules/`. Each rule that is used in any of the market betting groups
needs to be available and defined here.
