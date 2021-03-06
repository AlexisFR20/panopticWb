

class Person {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.cubes = {};
        this.construct();
    }

    construct() {
        const headSize = 8;
        const bodyWidth = 21;
        const bodyThickness = 8;
        const torsoHeight = 15;
        const legHeight = 15;
        const legThickness = 5;
        const chestSize = 16;
        const armHeight = 12;
        const armThickness = 3;
        const armGap = 2.5;
        const legGap = 5;
        
        const halfBodyWidth = bodyWidth * 0.55;

        this.dimensions = {
            headSize,
            bodyWidth,
            bodyThickness,
            torsoHeight,
            legHeight,
            legThickness,
            chestSize,
            armHeight,
            armThickness,
            armGap,
            legGap,
            halfBodyWidth,
        };

        const colors = ['var(--pplDark)', 'var(--pplMed)', 'var(--pplLight)', 'var(--pplLighter)', 'var(--pplDark)', 'var(--pplDark)'];
        const text = [];

        this.cubes.head = new Cube({
            x: 0,
            y:  halfBodyWidth - headSize,
            z: torsoHeight + legHeight,
            width: headSize,
            height: headSize,
            depth: headSize,
            colors,
            text,
            backside: true,
        });
        this.cubes['body'] = new Cube({
            x: 0,
            y: 0,
            z: legHeight,
            width: bodyThickness,
            height: torsoHeight,
            depth: chestSize,
            colors,
            text,
            backside: true,
        });
        this.cubes['left arm'] = new Cube({
            x: bodyThickness * 0.5 - armThickness * 0.5,
            y: -armThickness - armGap,
            z: torsoHeight + legHeight - armHeight,
            width: armThickness,
            height: armHeight,
            depth: armThickness,
            colors,
            text,
            backside: true,
        });
        this.cubes['right arm'] = new Cube({
            x: bodyThickness * 0.5 - armThickness * 0.5,
            y: chestSize + armGap,
            z: torsoHeight + legHeight - armHeight,
            width: armThickness,
            height: armHeight,
            depth: armThickness,
            colors,
            text,
            backside: true,
        });
        this.cubes['left leg'] = new Cube({
            x: legThickness / 2,
            y: halfBodyWidth - (legThickness + legGap),
            z: 0,
            width: legThickness,
            height: legHeight,
            depth: legThickness,
            colors,
            text,
            backside: true,
        });
        this.cubes['right leg'] = new Cube({
            x: legThickness / 2,
            y: legThickness + legGap,
            z: 0,
            width: legThickness,
            height: legHeight,
            depth: legThickness,
            colors,
            text,
            backside: true,
        });
        for (let cuKey in this.cubes) {
            const cube = this.cubes[cuKey];
            cube.x -= bodyThickness / 2;
        }
        const container = document.createElement('div');
        container.style.transformStyle = 'preserve-3d';
        container.style.transform = 'translate3d(0, 0, 0)';
        container.style.position = 'absolute';
        container.style.left = '0px';
        container.style.top = '0px';
        Object.keys(this.cubes).forEach((key) => {
            this.cubes[key].element = this.cubes[key].createElement();
            container.appendChild(this.cubes[key].element);
        });
        this.container = container;
        this.container.style.backgroundColor = 'red';
        this.container.classList.add('person');
        // this.container.style.transformOrigin = `0px 0px 0px`;
        this.container.style.transformOrigin = `0px 8px 0px`;
    }

    /**
     * 
     * @param {object} opt 
     * @param {number} opt.x - the x position
     * @param {number} opt.y - the y position
     * @param {number} opt.y - the y position
     * @param {number} opt.walkingFrameDelta - 0-1, the walking animation frame
     * @param {number} opt.directionAngle - the angle in degrees the person is facing
     */
    setRenderConfiguration({
        x = 0,
        y = 0,
        z = 0,
        walkingFrameDelta = 0,
        directionAngle = 0,
    }) {
        this.x = x;
        this.y = y;
        this.container.style.transform = `translate3d(${x}px, ${y}px, ${z}px) rotateZ(${directionAngle}deg) `;
        const la = this.cubes['left arm'].element;
        const ra = this.cubes['right arm'].element;
        const ll = this.cubes['left leg'].element;
        const rl = this.cubes['right leg'].element;

        var deg = Math.sin(walkingFrameDelta * 2 * Math.PI) * 8;
        var degL = Math.sin(walkingFrameDelta * 2 * Math.PI) * 10;
        const neckHeight = this.dimensions.legHeight + this.dimensions.torsoHeight;
        // la.style.transformOrigin = `${this.dimensions.bodyThickness/2}px 0px ${neckHeight}px`;
        la.style.transformOrigin = `0 0 0`;
        la.style.transform = `translate3d(${this.dimensions.armGap}px, ${0.5}px, ${neckHeight+5}px) rotateY(${deg+180}deg) translate3d(${0}px, 0px, ${-this.dimensions.armHeight}px)`;
        // ra.style.transformOrigin = `${this.dimensions.bodyThickness/2}px 0px ${neckHeight}px`;
        ra.style.transformOrigin = `0 0 0`;
        ra.style.transform = `translate3d(${this.dimensions.armGap}px, ${-0.5}px, ${neckHeight+5}px) rotateY(${-deg+180}deg)  translate3d(${0}px, 0px, ${-this.dimensions.armHeight}px)`;
        // ll.style.transformOrigin = `${this.dimensions.bodyThickness/2}px 0px ${this.dimensions.legHeight}px`;
        ll.style.transformOrigin = '0px 0px 0px';
        ll.style.transform = `translate3d(0px, 0px, ${this.dimensions.legHeight}px) rotateY(${-degL+180}deg)`;
        // rl.style.transformOrigin = `${this.dimensions.bodyThickness/2}px 0px ${this.dimensions.legHeight}px`;
        rl.style.transformOrigin = '0px 0px 0px';
        rl.style.transform = `translate3d(0px, 0px, ${this.dimensions.legHeight}px) rotateY(${degL+180}deg)`;
    }

    getBoundingBox() {
        const w = this.dimensions.bodyWidth;
        return new Bbox(this.x - w*0.5, this.y - w*0.5, w, w);
    }

    
    async addToMap(map) {
        map.addItem(this.container);
    }

    /**
     * creates a bounding box, of a person's dimensions
     * given a center point
     * @param {number} x - x loc of person
     * @param {number} y - y loc of person
     * @returns {Bbox}
     */
    static createBoundingBox(x, y) {
        const maxBodySize = 30;
        const halfBodySize = 15;
        return new Bbox(x - halfBodySize, y - halfBodySize, maxBodySize, maxBodySize);
    }
}