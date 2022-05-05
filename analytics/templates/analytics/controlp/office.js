
function Office(itemsCajones) {
    const officeHashMapOLD = `
    |                                                    |
    | a b c d     el  pt   xB   FK                       |
    | f g h i                                            |
    |             ^m  qu   yC   GL    P    QQQQ          |
    |                                 P    QQQQ          |
    | R S T U     jn  rv   zD   HM    P    QQQQ          |
    | V W X Y                         P                  |
    |             ko  sw   AE   IN    P                  |
    |                                 P                  |
    | Z { } [                   JO                       |
    | = ] ; /                                            |
    |                                                    |
    |             %%%% &&&& ----                         |
    | ! @ # $     %%%% &&&& ----                         |
    |             %%%% &&&& ----                         |`;
    const officeHashMap = `
    |                                                    |
    |                                                    |
    |                                                    |
    |                                                    |
    |                                                    |
    |       p                                            |
    |       p                                            |
    |       p                                            |
    |                                                    |
    |                                                    |
    | a b c d e f g h                                    |`;
    //const horizontalDesksMap = new Map('abcdfghiRSTUVWXYZ{}[]=/;!@#$'.split('').map(x => [x, true]));
    const horizontalDesksMap = new Map();
    const lines = officeHashMap.split('\n').slice(1);
    const items = new Map();

    const y = 3;
    let posX = 2;

    
    for(let x = 0; x < itemsCajones.length; x++){
        const letter = itemsCajones[x].idCajon; 
        let disp = itemsCajones[x].disponibilidad;;
        if(disp == "Ocupado"){
            items.set(letter, { x: posX, y, type: 'desk', letter, horiz: horizontalDesksMap.has(letter), color: 'red' });
        }else if(disp == "O/Caja vacía"){
            items.set(letter, { x: posX, y, type: 'desk', letter, horiz: horizontalDesksMap.has(letter), color: 'yellow' });
        }else{
            items.set(letter, { x: posX, y, type: 'desk', letter, horiz: horizontalDesksMap.has(letter), color: '#00a135' });
        }
        posX+=2;
    }
    /*for(let y = 0; y < lines.length; y++) {
        const row = lines[y].split('|')[1].split('');
        for(let x = 0; x < row.length; x++) {
            const letter = row[x];
            if (letter !== ' ') {
                if (items.has(letter)) {
                    const item = items.get(letter);
                    if (item.type === 'desk') {
                        items.set(letter, {
                            ...item,
                            type: 'block',
                            maxX: x,
                            maxY: y,
                        });
                    } else {
                        items.set(letter, {
                            ...item,
                            maxX: Math.max(x, item.maxX),
                            maxY: Math.max(y, item.maxY),
                        });
                    }
                } else {
                    items.set(letter, { x, y, type: 'desk', letter, horiz: horizontalDesksMap.has(letter) });
                }
            }
        }
    }*/

    const itemsArray = [...items.values()].map(item => {
        if (item.type === 'block') {
            return {
                ...item,
                width: (item.maxX - item.x) + 1,
                height: (item.maxY - item.y) + 1,
            };
        }
        return item;
    });
    return itemsArray;
}


