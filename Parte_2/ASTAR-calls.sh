BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[1;32m'
NC='\033[0m'

rm ASTAR-test/*.stat ASTAR-test/*.output
files=`ls ./ASTAR-test`
out='.csv'


echo -e "${GREEN}Executing all test cases in ASTAR-test${NC}"

for eachfile in $files; 
do
	path_to_file='./ASTAR-test/'$eachfile
	echo -e "$eachfile num_h=1 ${RED}[[Launched]]${NC}"
	python3 ASTARTraslados.py $path_to_file 1
	echo -e "$eachfile num_h=1 ${GREEN}[[Executed]]${NC}"
	echo -e "$eachfile num_h=2 ${RED}[[Launched]]${NC}"
	python3 ASTARTraslados.py $path_to_file 2
	echo -e "$eachfile num_h=2 ${GREEN}[[Executed]]${NC}"
	echo "######"  
done
