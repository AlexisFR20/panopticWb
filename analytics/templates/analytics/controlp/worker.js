importScripts(
    '/analytics/templates/analytics/controlp/worker_interface.js',
    '/analytics/templates/analytics/controlp/LLA.js',
    '/analytics/templates/analytics/controlp/Bbox.js',
    '/analytics/templates/analytics/controlp/person.js',
    '/analytics/templates/analytics/controlp/NavigatingPerson.js',
);

let workProcessor = null;

function start() {
    setInterval(() => {
        workProcessor.step();
    }, 20);
}

onmessage = function(ev) {
    const { data: message } = ev;

    if (message.type === 'init') {
        const initJson = message.initJson;
        workProcessor = new WorkProcessor(initJson, data => {
            postMessage(data);
        });
        start();
    } else if (message.type === 'job') {
        const data = message.data;
        if (workProcessor) {
            workProcessor.beginJob(data);
        }
    }
}
