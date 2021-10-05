
Build it:
```
DOCKER_BUILDKIT=0 sudo docker build -t palmid-lambda:latest .
```

Run it:
```
# When logged in with role
sudo docker run -e AWS_SECRET_ACCESS_KEY=[MY_SECRET] -e AWS_ACCESS_KEY_ID=[MY_ACCESS_KEY] -p 9000:8080 palmid-lambda:latest

# Or provide S3 credentials
sudo docker run -e AWS_SECRET_ACCESS_KEY=[MY_SECRET] -e AWS_ACCESS_KEY_ID=[MY_ACCESS_KEY] -p 9000:8080 palmid-lambda:latest
```


Call it:
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{ "sequence": ">SRR9968562_waxsystermes_virus_microassembly\nPIWDRVLEPLMRASPGIGRYMLTDVSPVGLLRVFKEKVDTTPHMPPEGMEDFKKASKEVE\nKTLPTTLRELSWDEVKEMIRNDAAVGDPRWKTALEAKESEEFWREVQAEDLNHRNGVCLR\nGVFHTMAKREKKEKNKWGQKTSRMIAYYDLIERACEMRTLGALNADHWAGEENTPEGVSG\nIPQHLYGEKALNRLKMNRMTGETTEGQVFQGDIAGWDTRVSEYELQNEQRICEERAESED\nHRRKIRTIYECYRSPIIRVQDADGNLMWLHGRGQRMSGTIVTYAMNTITNAIIQQAVSKD\nLGNTYGRENRLISGDDCLVLYDTQHPEETLVAAFAKYGKVLKFEPGEPTWSKNIENTWFC\nSHTYSRVKVGNDIRIMLDRSEIEILGKARIVLGGYKTGEVEQAMAKGYANYLLLTFPQRR\nNVRLAANMVRAIVPRGLLPMGRAKDPWWREQPWMSTNNMIQAFNQIWEGWPPISSMKDIK\nYVGRAREQMLDST", "hash": "waxsys_test"}'
```

Tag it:
```
sudo docker tag palmid-lambda:latest 797308887321.dkr.ecr.us-east-1.amazonaws.com/palmid-lambda:latest
```

Login to ECR (needs `aws configure` in beforehand):
```
aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 797308887321.dkr.ecr.us-east-1.amazonaws.com
```

Push it to AWS ECR:
```
sudo docker push 797308887321.dkr.ecr.us-east-1.amazonaws.com/palmid-lambda:latest
```

On AWS-Lambda configuration page, ensure the correct image is deployed.

Call it as AWS lambda (via API gateway --> URL is predefined in AWS). The `hash` attribute defines where it will be stored on S3:
```
curl -XPOST "https://b57b85pybb.execute-api.us-east-1.amazonaws.com/default/palmid-lambda" -d '{ "sequence": ">SRR9968562_waxsystermes_virus_microassembly\nPIWDRVLEPLMRASPGIGRYMLTDVSPVGLLRVFKEKVDTTPHMPPEGMEDFKKASKEVE\nKTLPTTLRELSWDEVKEMIRNDAAVGDPRWKTALEAKESEEFWREVQAEDLNHRNGVCLR\nGVFHTMAKREKKEKNKWGQKTSRMIAYYDLIERACEMRTLGALNADHWAGEENTPEGVSG\nIPQHLYGEKALNRLKMNRMTGETTEGQVFQGDIAGWDTRVSEYELQNEQRICEERAESED\nHRRKIRTIYECYRSPIIRVQDADGNLMWLHGRGQRMSGTIVTYAMNTITNAIIQQAVSKD\nLGNTYGRENRLISGDDCLVLYDTQHPEETLVAAFAKYGKVLKFEPGEPTWSKNIENTWFC\nSHTYSRVKVGNDIRIMLDRSEIEILGKARIVLGGYKTGEVEQAMAKGYANYLLLTFPQRR\nNVRLAANMVRAIVPRGLLPMGRAKDPWWREQPWMSTNNMIQAFNQIWEGWPPISSMKDIK\nYVGRAREQMLDST", "hash": "waxsys_test"}'
```
This call is set up asynchronously, so it gives you feedback directly, but it takes up to three Minutes to create and upload the report.

This will produce a report that will be accessible here, where the defined hash will be used as [hash].html:
```
https://s3.amazonaws.com/openvirome.com/MY_HASH.html
```

Call the wrapper, that handles the hashing functionality:
```
curl -XPOST "https://3niuza5za3.execute-api.us-east-1.amazonaws.com/default/api-lambda" -d '{ "sequence": ">SRR9968562_waxsystermes_virus_microassembly\nPIWDRVLEPLMRASPGIGRYMLTDVSPVGLLRVFKEKVDTTPHMPPEGMEDFKKASKEVE\nKTLPTTLRELSWDEVKEMIRNDAAVGDPRWKTALEAKESEEFWREVQAEDLNHRNGVCLR\nGVFHTMAKREKKEKNKWGQKTSRMIAYYDLIERACEMRTLGALNADHWAGEENTPEGVSG\nIPQHLYGEKALNRLKMNRMTGETTEGQVFQGDIAGWDTRVSEYELQNEQRICEERAESED\nHRRKIRTIYECYRSPIIRVQDADGNLMWLHGRGQRMSGTIVTYAMNTITNAIIQQAVSKD\nLGNTYGRENRLISGDDCLVLYDTQHPEETLVAAFAKYGKVLKFEPGEPTWSKNIENTWFC\nSHTYSRVKVGNDIRIMLDRSEIEILGKARIVLGGYKTGEVEQAMAKGYANYLLLTFPQRR\nNVRLAANMVRAIVPRGLLPMGRAKDPWWREQPWMSTNNMIQAFNQIWEGWPPISSMKDIK\nYVGRAREQMLDST"}'
```
The main difference here is, that no hash is needed, since it's generated via the RNA sequence input.

This then will lead to such response: `{"statusCode": 200, "body": "9afe3a5a2fadb13f709a7b9e148495092bb9f727"}` and therefore the report will be later available under [https://s3.amazonaws.com/openvirome.com/9afe3a5a2fadb13f709a7b9e148495092bb9f727.html]()