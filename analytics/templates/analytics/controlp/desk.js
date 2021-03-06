class Desk {
    /**
     * @constructor
     * @param {number} x 
     * @param {number} y 
     * @param {string} owner - a name written on the desk (the owner)
     * @param {string} horizontal 
     */
    constructor(x, y, owner, horizontal = false, color) {
        this.x = x;
        this.y = y;
        this.owner = owner;
        this.cubes = [];
        this.horizontal = horizontal;
        this.color = color;
        this.construct();
    }

    construct() {
        const height = 0;
        let width = 70;
        let length = 180;
        if (this.horizontal) {
            width = 95;
            length = 50;    
        }
        //const woodDepth = 0;
        const colors = [
            'var(--deskLegColor0)',
            'var(--deskLegColor1)',
            'var(--deskLegColor2)',
        ];
        const topColors = [
            '#FFFFFF',
            '#CCCCCC',
            '#BBBBBB',
        ];
        this.cubes.push(
           /* // leg btm rht
            new Cube({
                x: this.x + width - woodDepth,
                y: this.y + length - woodDepth,
                colors,
                text: ['', '', ''],
                width: woodDepth,
                height: height + woodDepth,
                depth: woodDepth,
            }),
            // leg btm lft
            new Cube({
                x: this.x,
                y: this.y + length - woodDepth,
                colors,
                text: ['', '', ''],
                width: woodDepth,
                height: height + woodDepth,
                depth: woodDepth,
            }),
            // leg top rht
            new Cube({
                x: this.x + width - woodDepth,
                y: this.y,
                colors,
                text: ['', '', ''],
                width: woodDepth,
                height: height + woodDepth,
                depth: woodDepth,
            }),
            // leg top lft
            new Cube({
                x: this.x,
                y: this.y,
                colors,
                text: ['', '', ''],
                width: woodDepth,
                height: height + woodDepth,
                depth: woodDepth,
            }),*/
            // top
            new Cube({
                x: this.x,
                y: this.y,
                colors: topColors,
                text: [`<div style="border:1px solid var(--deskOutline);width:100%;height:100%;color:var(--deskFontColor);background-color:${this.color};">${this.owner}</div>`, '', ''],
                width,
                height: 0,
                depth: length,
                z: height+1,
            }),
        );
    }

    /**
     * @returns {Bbox}
     */
    getBoundingBox() {
        if (!this._bbox) {
            const bbox = this.cubes[0].getBoundingBox();
            this._bbox = this.cubes.reduce((p, c) => Bbox.add(p, c.getBoundingBox()), bbox);
        }
        return this._bbox;
    }

    get elements() {
        return this.cubes.map(cube => cube.createElement());
    }

    addToMap(map) {
        this.elements.forEach(el => map.addItem(el));
    }
}