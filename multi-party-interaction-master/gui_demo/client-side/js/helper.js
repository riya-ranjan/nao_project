function toggleButtons(buttonsEnabled = true, buttons = null) {
    if (!buttons){
        buttons = document.querySelectorAll("button");
    }
    console.log(buttons.length);

    buttons.forEach((button) => {
        button.disabled = !buttonsEnabled;
    });
}

function addToDisplayList(list, content, style) {
    let li = document.createElement("li");
    let text = document.createElement("p");
    text.innerHTML = content;
    if (text.style.cssText === undefined || text.style.cssText === null)
        text.style.cssText = "";
    text.style.cssText += style;

    li.appendChild(text);
    list.appendChild(li);
}

function drawGrid(context, gridInterval, padding = 0, lineWidth = 1) {
    let lineOffset = lineWidth / 2;

    // draw vertical lines
    for (let x = 0; x <= context.canvas.clientWidth; x += gridInterval) {
        context.moveTo(lineOffset + x + padding, padding);
        context.lineTo(lineOffset + x + padding, context.canvas.clientWidth + padding);
    }

    // draw horizontal lines
    for (let y = 0; y <= context.canvas.clientHeight; y += gridInterval) {
        context.moveTo(padding, lineOffset + y + padding);
        context.lineTo(context.canvas.clientWidth + padding, lineOffset + y + padding);
    }

    // set grid line color to gray
    context.strokeStyle = "gray";
    context.stroke();
}