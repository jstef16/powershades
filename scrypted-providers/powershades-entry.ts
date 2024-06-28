// https://developer.scrypted.app/#getting-started
import dgram = require('dgram');
import { Entry, EntrySensor, ScryptedDeviceBase, DeviceProvider, Refresh, ScryptedDeviceType, ScryptedInterface, sdk, ScryptedNativeId } from '@scrypted/sdk';

console.log('This will create a virtual powershades window covering.');

class PowerShade extends ScryptedDeviceBase implements Entry, EntrySensor, Refresh {
    constructor(nativeId?: string) {
        super(nativeId);
        this.on = this.on || false;
        this.ipAddr = this.info?.ip;
        this.socket = dgram.createSocket('udp4');
    }

    ipAddr: string | undefined;
    port = 42;
    private socket: dgram.Socket;

    allTheWayOpen = '0a005a7d1a0d000001006400000000000000';
    mostlyOpen = '0a00312a1a0d000001005800000000000000';
    allTheWayClosed = '0a008fff1a0d000001000000000000000000';

    stateIndicator = 29;
    getState = '0a00898f1d0d000001000000000000000000';

    async closeEntry() {
        try {
            this.sendUdpRequest(this.allTheWayClosed);
        } catch (_e) {
            this.console.log(_e);
        }
        this.entryOpen = false
    }

    async openEntry() {
        try {
            this.sendUdpRequest(this.allTheWayOpen);
        } catch (_e) {
            this.console.log(_e);
        }
        this.entryOpen = true
    }

    sendUdpRequest(message: string) {

        let isInitialRequest = false;
        try {
            this.socket.address();
        } catch (_e) {
            this.console.log("Socket is not bound. Will subscribe to messages after request");
            isInitialRequest = true;
        }

        this.socket.send(Buffer.from(message, 'hex'), this.port, this.ipAddr, (err, bytes) => {
            console.log('UDP error: %s', err);
            console.log('UDP bytes: %s', bytes);
            // this.console.log('Port used by UDP client: ', this.socket.address().port);
            if (isInitialRequest) {
                this.console.log("Subscribing socket to messages at %s:%n", this.ipAddr, this.socket.address().port);
                this.subscribeUdpSocket(this.ipAddr, this.socket.address().port);
            }
        });
    }

    async getRefreshFrequency(): Promise<number> {
        this.console.log('Returned refresh frequency');
        return 15;
    }

    async refresh(refreshInterface: string, userInitiated: boolean): Promise<void> {
        try {
            this.sendUdpRequest(this.getState);
        } catch (_e) {
            this.console.log(_e);
        }
    }

    subscribeUdpSocket(ipAddr: string | undefined, port: number | undefined) {

        this.console.log('Subscribing UDP socket to requests')

        // Handle incoming messages
        this.socket.on('message', (msg, rinfo) => {
            // console.log(`UDP socket received: ${msg.toString('hex')} from ${rinfo.address}:${rinfo.port}`);

            if (msg[4] == this.stateIndicator) {
                let percentage = msg[8];
                // this.console.log(`Current percent open: ${percentage}%`)
                this.entryOpen = percentage == 100
            }
        });

        // Handle errors
        this.socket.on('error', (err) => {
            console.error('UDP socket error:', err);
        });
    }
}

class PowerShadeProvider extends ScryptedDeviceBase implements DeviceProvider {
    constructor(nativeId?: string) {
        super(nativeId);
        this.prepareDevices();
    }

    async prepareDevices() {
        await sdk.deviceManager.onDevicesChanged({
            devices: [
                {
                    nativeId: 'livingRoomShade',
                    name: 'Living Room Shade',
                    type: ScryptedDeviceType.WindowCovering,
                    interfaces: [
                        ScryptedInterface.Entry,
                        ScryptedInterface.EntrySensor,
                        ScryptedInterface.Refresh
                    ],
                    info: {
                        ip: '192.168.1.80'
                    }
                },
                {
                    nativeId: 'bedroomShade',
                    name: 'Bedroom Shade',
                    type: ScryptedDeviceType.WindowCovering,
                    interfaces: [
                        ScryptedInterface.Entry,
                        ScryptedInterface.EntrySensor,
                        ScryptedInterface.Refresh
                    ],
                    info: {
                        ip: '192.168.1.71'
                    }
                },
                {
                    nativeId: 'loftShade',
                    name: 'Loft Shade',
                    type: ScryptedDeviceType.WindowCovering,
                    interfaces: [
                        ScryptedInterface.Entry,
                        ScryptedInterface.EntrySensor,
                        ScryptedInterface.Refresh
                    ],
                    info: {
                        ip: '192.168.1.69'
                    }
                },
                {
                    nativeId: 'officeShade',
                    name: 'Office Shade',
                    type: ScryptedDeviceType.WindowCovering,
                    interfaces: [
                        ScryptedInterface.Entry,
                        ScryptedInterface.EntrySensor,
                        ScryptedInterface.Refresh
                    ],
                    info: {
                        ip: '192.168.1.66'
                    }
                }
            ]
        });
    }

    async getDevice(nativeId: string) {
        return new PowerShade(nativeId);
    }

    releaseDevice(id: string, nativeId: ScryptedNativeId): Promise<void> {
        throw new Error('Release device method not implemented.');
    }
}

export default PowerShadeProvider;
