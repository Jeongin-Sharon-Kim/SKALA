
function showMyBag() {
    const myBag = [
    {name: "립스틱", count: 3},
    {name: "데일밴드", count: 5},
    {name: "지갑", count: 1}
];

resultext = "👜 [내 가방 속 물품 목록]\n\n";
document.write(resultext + "<br>");

for (let item of myBag) {
    document.write("- " + item.name + ": " + item.count + "개<br>");
}

document.write("<br>총 물품 종류: " + myBag.length + "가지");
}

showMyBag();





