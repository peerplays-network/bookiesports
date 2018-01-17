Schema
======

For validation of the data format presented in the sports folder, a
validation is performed. The corresponding validation schemata are
stored in the  ``schema/`` subdirectory and used internally when
instantiating :class:`bookiesports.BookieSports`.

Schemata
--------

Genera definitions
__________________
.. literalinclude:: ../bookiesports/schema/definitions.yaml
   :language: yaml

Sport
_____
.. literalinclude:: ../bookiesports/schema/sport.yaml
   :language: yaml

Eventgroup
__________
.. literalinclude:: ../bookiesports/schema/eventgroup.yaml
   :language: yaml

Participant
___________
.. literalinclude:: ../bookiesports/schema/participant.yaml
   :language: yaml

Rule
____
.. literalinclude:: ../bookiesports/schema/rule.yaml
   :language: yaml

BettingMarketGroup
__________________
.. literalinclude:: ../bookiesports/schema/bettingmarketgroup.yaml
   :language: yaml
