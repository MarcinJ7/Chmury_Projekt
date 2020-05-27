 module.exports = async function (context, req) {
    try {
        if (req.body && (req.body.imageEncoded || req.body.imageUrl)) {
            const request = require('request-promise');
            let imageUrl;
            let blockService;
            if (req.body.imageEncoded) {
                const fs = require('fs');
                const Readable = require('stream').Readable;
                const { BlobServiceClient, StorageSharedKeyCredential } = require('@azure/storage-blob');

                const account = 'blobprojekt';
                const accountKey = 'LICebmDrCg3c4RQPd0dyLwNeBC01x3YlVGdkZ+mR2tAgza8SP/5+UJbKPE7ZLAnHNduYzc6gxVCvsYniB4J2jg==';
                
                const sharedKeyCredential = new StorageSharedKeyCredential(account, accountKey);
                const blobServiceClient = new BlobServiceClient(
                    `https://${account}.blob.core.windows.net`,
                    sharedKeyCredential
                );

                const buffer = Buffer.from(req.body.imageEncoded, 'base64');
                const s = new Readable()
                s.push(buffer);   
                s.push(null);

                const containerService = blobServiceClient.getContainerClient('zdjecia');
                blockService = containerService.getBlockBlobClient(`file-${new Date().getTime()}`);
                await blockService.uploadStream(s);
                imageUrl = blockService.url;
            } else {
                imageUrl = req.body.imageUrl;
            }

            const params = {
                returnFaceId: 'true',
                returnFaceLandmarks: 'false',
                returnFaceAttributes: 'age'
            };

            const optionsCS = {
                uri: 'https://comparetomodelapi.cognitiveservices.azure.com/face/v1.0/detect',
                qs: params,
                body: `{"url":"${imageUrl}"}`,
                headers: {
                    'Content-Type': 'application/json',
                    'Ocp-Apim-Subscription-Key' : '883d7d70ea45461badcb680bf2f3e180'
                },
            };

             const optionsDocker = {
                uri: 'http://52.183.217.150:5000',
                body: `{"url":"${imageUrl}"}`,
                headers: {
                    'Content-Type': 'application/json'
                },
            };

            const r = await request.post(optionsCS);
            const r2 = await request.post(optionsDocker);
            const response = JSON.parse(r || '');
            const response2 = JSON.parse(r2 || '');
            if (blockService) {
                await blockService.delete();
            }

            if (!response || !response2) {
                context.res = {
                    status: 500,
                    body: {
                        error: 'Service error'
                    }
                }
            } else {
                context.res = {
                    body: {
                        ageCS: response.map(el => `${el.faceAttributes.age}`).join(', '),
                        ageDocker: response2.age
                    }
                };
            }
        }
    } catch (err) {
        context.res = {
            status: 500,
            body: {
                error: err ? err.message || JSON.stringify(err) : ''
            }
        }
    }
};