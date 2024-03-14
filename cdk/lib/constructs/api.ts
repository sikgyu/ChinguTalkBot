import { Construct } from "constructs";
import { ITable } from "aws-cdk-lib/aws-dynamodb";
import { HttpApi, CorsHttpMethod, HttpMethod } from "aws-cdk-lib/aws-apigatewayv2";
import { HttpUserPoolAuthorizer } from 'aws-cdk-lib/aws-apigatewayv2-authorizers';
import { CfnOutput, Duration } from "aws-cdk-lib";
import { Auth } from "./auth";


export interface ApiProps {
    readonly database: ITable;
    readonly corsAllowOrigins?: string[];
    readonly auth: Auth;
    readonly bedrockRegion: string;
    readonly bedrockEndpointUrl: string;
  }


export class Api extends Construct {
    readonly api: HttpApi;
    constructor(scope: Construct, id: string, props: ApiProps) {
      super(scope, id);
  
      const { database, corsAllowOrigins: allowOrigins = ["*"] } = props;

  
      const api = new HttpApi(this, "HttpApi", {
        corsPreflight: {
          allowHeaders: ["*"],
          allowMethods: [
            CorsHttpMethod.GET,
            CorsHttpMethod.HEAD,
            CorsHttpMethod.OPTIONS,
            CorsHttpMethod.POST,
            CorsHttpMethod.PUT,
            CorsHttpMethod.PATCH,
            CorsHttpMethod.DELETE,
          ],
          allowOrigins: allowOrigins,
          maxAge: Duration.days(10),
        },
      });
  
      const authorizer = new HttpUserPoolAuthorizer(
        "Authorizer",
        props.auth.userPool,
        {
          userPoolClients: [props.auth.client],
        }
      );
      let routeProps: any = {
        path: "/{proxy+}",
        methods: [
          HttpMethod.GET,
          HttpMethod.POST,
          HttpMethod.PUT,
          HttpMethod.PATCH,
          HttpMethod.DELETE,
        ],
        authorizer,
      };
    
      this.api = api;
  
      new CfnOutput(this, "BackendApiUrl", { value: api.apiEndpoint });
    }
  }