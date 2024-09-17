# SMA-EM daemon features

this page should give an overview of maintained features.
other features untested because I do not have the appropriate hardware / software could be found in features-outdated.

All the desired features must be activated in the configuration file
```
[SMA-EM]
# list of features to load/run
features=simplefswriter nextfeature
```
Each feature has it own configuration section  in the configuration-file.

[FEATURE-featurename]

please have a look at the config.sample file or have a look at the features file (description) for supported configuration options.

```
[FEATURE-simplefswriter]
# list serials simplefswriter notice
serials=1900204522
# measurement vars simplefswriter should write to filesystem (only from smas with serial in serials)
values=pconsume psupply qsupply ssupply
```

Feature fist

## mqtt.py
send SMA-measurement-values to an mqtt broker.

## simplefswriter.py
writes configureable measurement-values to the filesystem

