# ttf-render-demo
A demo of how to render unicode string from ttf to svg path, pure python implemented

```
git clone https://github.com/teach-myself/ttf-render-demo
pip3 install fonttools
cd ttf-render-demo
python3 main.py
```

this will finally generate:
```
M 1001 -305 L 1001 -66 Q 1001 54 975 146 Q 950 238 893 317 L 708 317 Q 767 246 804 161 Q 841 76 841 0 L 712 0 L 712 -305 Z M 2367 0 L 2095 0 Q 2091 -15 2085 -75 Q 2080 -136 2080 -176 L 2076 -176 Q 1985 20 1730 20 Q 1541 20 1438 -127 Q 1335 -275 1335 -540 Q 1335 -809 1443 -955 Q 1552 -1102 1751 -1102 Q 1866 -1102 1949 -1054 Q 2033 -1006 2078 -911 L 2080 -911 L 2078 -1089 L 2078 -1484 L 2359 -1484 L 2359 -236 Q 2359 -136 2367 0 Z M 2082 -547 Q 2082 -722 2023 -816 Q 1965 -911 1851 -911 Q 1738 -911 1683 -819 Q 1628 -728 1628 -540 Q 1628 -172 1849 -172 Q 1960 -172 2021 -269 Z
```

Copy this svg path, and see results on https://yqnn.github.io/svg-path-editor/
