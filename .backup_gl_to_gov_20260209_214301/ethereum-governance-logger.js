// 使用Ethereum记录关键治理操作
const governLog = new web3.eth.Contract(governanceABI, contractAddress);

function logGovernanceAction(action, actor, target) {
  governLog.methods.logAction(
    action, 
    actor, 
    target,
    Math.floor(Date.now()/1000)
  ).send({from: governanceAccount});
}
