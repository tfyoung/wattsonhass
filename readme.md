Wattson Solar Plus from DIY Kyoto component for Home assistant.

# Installation

Place the contents of this in config/custom_components/wattson
Plug in the Wattson via USB.
Restart hass

# Thanks

Based off the serial protocol in https://github.com/sapg/openwattson

# About/Known issues

I found my usage seemed to be 1/4 of what was on the display so that's multiplied by 4.
It will only load the 1st wattson device found pluged in via USB. This works for me, but certainly isn't the best code or implementation.
Given it's an old device that's no longer sold, I don't intend to improve this unless someone else has issues. Feel free to contact me or file an issue.
