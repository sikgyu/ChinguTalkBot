#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { ChinguTalkStack } from "../lib/cdk-stack";

const app = new cdk.App();

const BEDROCK_REGION = app.node.tryGetContext("bedrockRegion");
const BEDROCK_ENDPOINT_URL = app.node.tryGetContext("bedrockEndpointUrl");

new ChinguTalkStack(app, `ChinguTalkStack`, {
  bedrockRegion: BEDROCK_REGION,
  bedrockEndpointUrl: BEDROCK_ENDPOINT_URL,
});