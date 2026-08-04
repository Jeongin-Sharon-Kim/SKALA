
var computerNum = Math.floor(Math.random() * 50) + 1;// 1~50까지의 랜덤 숫자 생성
// 사용자에게 입력받기
var userNum = prompt("1~50 사이의 숫자를 입력하세요:");
//맞출 때 까지 반복, 맞추면 축하+몇번만에 맞췄는지 알려주기
var cnt = 1;
while (userNum != computerNum) {
    if (userNum < computerNum) {
    userNum = prompt("Up!");
} 
    else if (userNum > computerNum) {
    userNum = prompt("Down!");
}
cnt++;
}
alert("축하합니다! " + cnt + " 번 만에 맞췄습니다!");