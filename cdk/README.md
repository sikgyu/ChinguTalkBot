## Environment Setup

To create CDK, I used the following code:

```jsx
mkdir cdk
cd cdk
npm install -g aws-cdk
cdk init app --language typescript
```

**constructs directory**

The directory is structured to maintain modular constructs, making the infrastructure code more manageable and scalable. I created constructs directory in the lib folder and added `auth.ts` file.

**Key Componenets:**

- **UserPool:** Defines the user pool with specific password policies and sign-in options, facilitating self-signup and ensuring security standards.
- **UserPoolClient:** Creates a client application within the user pool to manage user interactions and session handling.

**Outputs:**

- **UserPoolId:** The identifier for the created user pool.
- **UserPoolClientId:** The identifier for the user pool client application.


## **Integration into CDK Stack**

The Auth construct is integrated into the main CDK stack, **`ChinguTalkStack`**, to provision the necessary AWS Cognito resources:

```jsx
const auth = new Auth(this, "Auth");
```


### **CDK Deployment**

After defining our infrastructure as code using AWS CDK, we proceed with deploying our resources to the cloud. This process is handled by the **`cdk deploy`** command. Here’s how we executed the deployment for our project:

1. Navigate to your project's root directory in the terminal.
2. Run the **`cdk deploy`** command.
    
    ```bash
    bashCopy code
    cdk deploy
    
    ```