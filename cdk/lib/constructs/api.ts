import { Construct } from "constructs";
import { HttpApi, CorsHttpMethod } from "aws-cdk-lib/aws-apigatewayv2";
import { CfnOutput, Duration } from "aws-cdk-lib";
import { Auth } from "./auth";


export interface ApiProps {
    readonly auth: Auth;
  }


export class Api extends Construct {
  readonly api: HttpApi;

  constructor(scope: Construct, id: string, props: ApiProps) {
    super(scope, id);

    // Create API instance
    this.api = new HttpApi(this, "HttpApi", {
      corsPreflight: {
        allowHeaders: ["Content-Type"],
        allowMethods: [CorsHttpMethod.GET, CorsHttpMethod.POST, CorsHttpMethod.OPTIONS],
        allowOrigins: ["*"],
        maxAge: Duration.days(10),
      },
    });

    // API endpoint
    new CfnOutput(this, "ApiEndpoint", {
      value: this.api.apiEndpoint,
    });
  }
}