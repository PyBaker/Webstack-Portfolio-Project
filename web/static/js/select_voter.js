document.getElementById("sendbutton").addEventListener('click', () => {
    let image = canvas.toDataURL();
    let r = new XMLHttpRequest();
    r.open("POST", "http://127.0.0.1:5000/truthMask", true);
    r.onreadystatechange = function () {
        if (r.readyState != 4 || r.status != 200) return;
        //alert("Success: " + r.responseText);
        console.log("sent");
    };
    r.send(input="test");
});
