import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Auth } from "./constructs/auth";
import { Api } from "./constructs/api";


export class ChinguTalkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    const auth = new Auth(this, "Auth");
    const api = new Api(this, "Api", {
      auth: auth,
    });

    new cdk.CfnOutput(this, "ApiEndpoint", {
      value: api.api.apiEndpoint
    });
  }
}
