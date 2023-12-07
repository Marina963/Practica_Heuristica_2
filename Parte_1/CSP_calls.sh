BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[1;32m'
NC='\033[0m'

files=`ls ./CSP-test`
csv='.csv'

echo -e "${GREEN}Executing all test cases in CSP-test${NC}"
for eachfile in $files; 
do
	if [[ $eachfile != *$csv* ]]; then
		path_to_file='./CSP-test/'$eachfile
		echo -e "$eachfile ${RED}[[Launched]]${NC}"
		python3 main.py $path_to_file
		echo -e "$eachfile ${GREEN}[[Executed]]${NC}" 
	fi
done
