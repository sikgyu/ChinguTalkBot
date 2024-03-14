import { StackProps } from "aws-cdk-lib";
import { Construct } from 'constructs';
import { Auth } from "./constructs/auth";
import { Api } from "./constructs/api";
import { Database } from "./constructs/database";
import * as cdk from "aws-cdk-lib";

export interface BedrockChatStackProps extends StackProps {
  readonly bedrockRegion: string;
  readonly bedrockEndpointUrl: string;
}

export class ChinguTalkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: BedrockChatStackProps) {
    super(scope, id, props);


    const auth = new Auth(this, "Auth");
    const database = new Database(this, "Database");
    const backend = new Api(this, "BackendApi", {
      database: database.table,
      auth,
      bedrockRegion: props.bedrockRegion,
      bedrockEndpointUrl: props.bedrockEndpointUrl,
    });


  }
}