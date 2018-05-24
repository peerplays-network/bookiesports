# Development

This file contains a few tips and tricks dor development.

## Change all assets easily:

    grep -lri "asset:" . | xargs sed -i "s/BTC/BTF/"
