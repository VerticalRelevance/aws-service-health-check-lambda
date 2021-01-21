# aws-service-health-check-lambda

This is a proof of concept tool to detect service / region level outages within an AWS environment. Refer to below as well as [Blog Post](https://www.verticalrelevance.com/insights/ "Blog Post") on this tool for more information.
                    
## Config File Generation
Use [Config Generator](https://docs.google.com/spreadsheets/d/1cGOPU9G-8ST0rNFs01Kw756kQkpsyDA8NIpWcRFQXiw/edit?usp=sharing "Config Generator")

### Application Service Tiers

#### Platinum Service
Services critical to your existing architecture and workload. Availability issues affecting a singular critical services result in a defined failover action and notification.
#### Gold Service
Services that are non-essential to your existing production architecture and workload, but if failed would result in sub-optimal operating conditions.
#### Silver Service
Auxiliary services within an architecture and workload. Have no functional or operational impact on existing workload. Losing these services will not result in any sort of resiliency event but will result in a notification.

------------


The ini configuration file requires that select AWS services are specified for the differnet application service tiers. For each service that is being leveraged, use the service shortname specified in the Health API Identifier inside the configuration file.
                    
AWS Service  | Health API Identifier
------------- | -------------
Alexa for Business | A4B
Abuse | ABUSE
Account | ACCOUNT
Activate Console | ACTIVATECONSOLE
Amplify | AMPLIFY
API Gateway | APIGATEWAY
AppFlow | APPFLOW
Application Discovery Service | DISCOVERY
Application Insights | APPLICATIONINSIGHTS
Application Autoscaling | APPLICATION_AUTOSCALING
App Mesh | APPMESH
AppStream 2.0 | APPSTREAM2
Appstream | APPSTREAM
AppSync | APPSYNC
Athena | ATHENA
Auto Scaling | AUTOSCALING
Alexa Web Information Service | AWIS
Backup | BACKUP
Batch | BATCH
Billing | BILLING
Braket | BRAKET
Certificate Manager | ACM
Chatbot | CHATBOT
Chime | CHIME
Client VPN | CLIENT_VPN
Cloud9 | CLOUD9
Cloud Directory | CLOUDDIRECTORY
CloudFormation | CLOUDFORMATION
CloudFront | CLOUDFRONT
CloudHSM | CLOUDHSM
CloudSearch | CLOUDSEARCH
CloudTrail | CLOUDTRAIL
CloudWatch | CLOUDWATCH
CodeArtifact | CODEARTIFACT
CodeBuild | CODEBUILD
CodeCommit | CODECOMMIT
CodeDeploy | CODEDEPLOY
CodeGuru Reviewer | CODEGURU_REVIEWER
CodePipeline | CODEPIPELINE
CodeStar | CODESTAR
Cognito | COGNITO
Comprehend | COMPREHEND
Comprehend Medical | COMPREHENDMEDICAL
Config | CONFIG
Connect | CONNECT
Control Tower | CONTROLTOWER
Database Migration Service | DMS
Data Exchange | DATAEXCHANGE
Data Lifecycle Manager | DLM
Data Pipeline | DATAPIPELINE
DataSync | DATASYNC
DeepComposer | DEEPCOMPOSER
DeepLens | DEEPLENS
DeepRacer | DEEPRACER
Detective | DETECTIVE
Device Farm | DEVICEFARM
Direct Connect | DIRECTCONNECT
Directory Service | DS
DocumentDB (with MongoDB compatibility) | DOCDB
DynamoDB | DYNAMODB
DynamoDB Accelerator (DAX) | DAX
Elastic Block Store (EBS) | EBS
EC2 | EC2
EC2 Image Builder | IMAGEBUILDER
Elastic File System (EFS) | ELASTICFILESYSTEM
ElastiCache | ELASTICACHE
Elastic Beanstalk | ELASTICBEANSTALK
Elastic Container Registry | ECR
Elastic Container Service | ECS
ECS Service Discovery | SERVICEDISCOVERY
Elastic Kubernetes Service | EKS
Elastic Load Balancing | ELASTICLOADBALANCING
Elastic MapReduce | ELASTICMAPREDUCE
Elasticsearch Service | ES
Elastic Transcoder | ELASTICTRANSCODER
Elemental MediaConnect | MEDIACONNECT
Elemental MediaConvert | MEDIACONVERT
Elemental MediaLive | MEDIALIVE
Elemental MediaPackage | MEDIAPACKAGE
Elemental MediaStore | MEDIASTORE
Elemental MediaTailor | MEDIATAILOR
EventBridge | EVENTS
Firewall Manager | FMS
Forecast | FORECAST
FreeRTOS | FREERTOS
FSx | FSX
GameLift | GAMELIFT
Global Accelerator | GLOBALACCELERATOR
Glue | GLUE
Glue DataBrew | DATABREW
Greengrass | GREENGRASS
Ground Station | GROUNDSTATION
GuardDuty | GUARDDUTY
Identity and Access Management | IAM
Import/Export | IMPORTEXPORT
Inspector | INSPECTOR
Inter-Region VPC Peering | INTERREGIONVPCPEERING
Interactive Video Service | IVS
Internet Connectivity | INTERNETCONNECTIVITY
IoT 1-Click | IOT1CLICK
IoT Analytics | IOT_ANALYTICS
IoT Core | IOT
IoT Device Defender | IOT_DEVICE_DEFENDER
IoT Device Management | IOT_DEVICE_MANAGEMENT
IoT Events | IOT_EVENTS
IoT SiteWise | IOT_SITEWISE
IoT Things Graph | IOTTHINGSGRAPH
IQ | IQ
Kafka | KAFKA
Kendra | KENDRA
Key Management Service | KMS
Keyspaces (for Apache Cassandra) | CASSANDRA
Kinesis | KINESIS
Kinesis Analytics | KINESISANALYTICS
Kinesis Data Streams | KINESISSTREAMS
Kinesis Firehose | FIREHOSE
Kinesis Video Streams | KINESIS_VIDEO
Lakeformation | LAKEFORMATION
Lambda | LAMBDA
Lex | LEX
License Manager | LICENSE_MANAGER
Lightsail | LIGHTSAIL
Machine Learning | MACHINELEARNING
Macie | MACIE
Managed Blockchain | MANAGEDBLOCKCHAIN
Management Console | MANAGEMENTCONSOLE
Marketplace | MARKETPLACE
Migration Hub | MGH
Mobile Hub | MOBILEHUB
Mobile Analytics | MOBILEANALYTICS
Mobile Targeting | MOBILETARGETING
MQ | MQ
NAT Gateway | NATGATEWAY
Neptune | NEPTUNE
Network Firewall | NETWORKFIREWALL
Opsworks | OPSWORKS
Opsworks Chef | OPSWORKS_CHEF
Opswork Puppet | OPSWORKS_PUPPET
Organizations | ORGANIZATIONS
Personal Health Dashboard | HEALTH
Personalize | PERSONALIZE
Polly | POLLY
Quantum Ledger Database (QLDB) | QLDB
Quicksight | QUICKSIGHT
Resource Access Manager (RAM) | RAM
Resource Groups | RESOURCE_GROUPS
RDS | RDS
Redshift | REDSHIFT
Rekognition | REKOGNITION
Risk | RISK
RoboMaker | ROBOMAKER
Route 53 | ROUTE53
Route 53 Domain Name Registration | ROUTE53DOMAINREGISTRATION
Route 53 Private DNS | ROUTE53PRIVATEDNS
Route 53 Resolver | ROUTE53RESOLVER
Simple Storage Service (S3) | S3
S3 Glacier | GLACIER
S3 Outposts | S3_OUTPOSTS
SageMaker | SAGEMAKER
Secrets Manager | SECRETSMANAGER
Security Hub | SECURITYHUB
Serverless Application Repository | SERVERLESSREPO
Server Migration Service | SMS
Service Catalog | SERVICECATALOG
Simple Email Service (SES) | SES
Shield | SHIELD
SimpleDB | SDB
Security | SECURITY
Service Quotas | SERVICEQUOTAS
Simple Workflow Service | SWF
Single Sign-On | SSO
Snowball | SNOWBALL
Simple Notification Service (SNS) | SNS
Simple Queue Service (SQS) | SQS
States | STATES
Storage Gateway | STORAGEGATEWAY
Sumerian | SUMERIAN
Support Center | SUPPORTCENTER
Systems Manager | SSM
Tag | TAG
Textract | TEXTRACT
Timestream | TIMESTREAM
Transcribe | TRANSCRIBE
Transfer Family | TRANSFER
Transit Gateway | TRANSIT_GATEWAY
Translate | TRANSLATE
Trusted Advisor | TRUSTEDADVISOR
VPC | VPC
VPC Private Link | VPCE_PRIVATELINK
VPN | VPN
WAF | WAF
Well-Architected Tool | WELLARCHITECTED
WorkDocs | WORKDOCS
WorkLink | WORKLINK
WorkMail | WORKMAIL
WorkSpaces | WORKSPACES
X-Ray | XRAY

