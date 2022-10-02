#! /bin/bash
#export DOCKER_YML=~/projects/strategies_github/donjonson_ftstrats_git/donjonson_ftstrats/util/docker-compose.yml
#export GENDOCKER=~/projects/strategies_github/donjonson_ftstrats_git/donjonson_ftstrats/util/
export DOCKER_YML=~/Projects/util/docker-compose.yml
export GENDOCKER=~/Projects/util/
function printme {
	echo $*
}

function freqtrade {
	if ! test -f ./docker-compose.yml
	then ln -s $DOCKER_YML docker-compose.yml
	fi
	docker-compose run --rm freqtrade $*
}


function freqtrade_up {
	if  test -f ./docker-compose.yml
	then rm -f ./docker-compose.yml
	fi
	python3 $GENDOCKER/gendockerfile.py $*
	docker-compose up
}

#alias="if ! test -f ./docker-compose.yml ; then ln -s $DOCKER_YML docker-compose.yml; fi;docker-compose -f $DOCKER_YML -bind ${pwd}:/user_data run --rm freqtrade "
