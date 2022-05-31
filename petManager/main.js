const { spawn } = require('node:child_process');
let myPuppet;

function runMePlz(comportment, size=[]){
	let parameters = ['CodePet.py'];
	parameters.push("-c");
	for(let tmp of comportment){
		parameters.push(tmp);
	}
	
	parameters.push("-s");
	for(let tmp of size){
		parameters.push(tmp);
	}
	
	myPuppet = spawn('python.exe', parameters);

	myPuppet.stdout.on('data', (data) => {
	  console.log(data.toString());
	});

	myPuppet.stderr.on('data', (data) => {
	  console.error(data.toString());
	});

	myPuppet.on('exit', (code) => {
	  console.log(`Child exited with code ${code}`);
	});
}

function killmeplz(){
	myPuppet.kill('SIGINT');
}

async function wait(time){
	return new Promise(function(resolve, reject){
		setTimeout(function(){
			resolve();
		}, time);
	});
}


async function main(){
	runMePlz([1, 0]);
	await wait(3000);
	killmeplz();
	runMePlz([1, 14]);
	await wait(3000);
	killmeplz();
}

main();
