#!/bin/bash

for i in {40000..90000};
do
    curl "http://webcache.googleusercontent.com/search?q=cache:https://kater.me/d/$i&vwsrc=0" \
    -H 'Connection: keep-alive' \
    -H 'Cache-Control: max-age=0' \
    -H 'Upgrade-Insecure-Requests: 1' \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
    -H 'Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja-JP;q=0.5,ja;q=0.4' \
    -H 'Cookie: CGIC=Inx0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; GOOGLE_ABUSE_EXEMPTION=ID=6f2491bd0b71d32d:TM=1595959310:C=r:IP=218.161.61.176-:S=APGng0uI4Iahx7T_JhCd8qVSYOXBsyDLuw; NID=204=yXj-eVg66560fDWYu8xontwkkUEiDIYxVHEAoo4T1jErNtkoYGSfaZdneW6k8yFRuliuChU3AScUfiouMogd38aQzorC36Ok6sF8ku3du1qjUW6uR1S_NF_8ln5Ap0A6O5podp1T3pJf50ZVW9eTknd7g2Pt8SESRqppMciPkpg' \
    --compressed \
    --insecure \
    --output ./d/$i.html \
    2> /dev/null;

    echo -ne "\b\b\b\b\b$i";
done