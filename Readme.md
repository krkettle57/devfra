# Devfra: Development infrastructure created by Terraform

## Terraform: Usage

前提

- 低コストを重視しアクセスキーを発行した
- セキュリティを重視しプライベートな Terraform 実行用インスタンスを作成しても OK

1. AWS: ローカル実行用に IAM ユーザを作成

- API キーを発行
- `sts.AssumeRole`のみを許可
- MFA デバイスを有効化

2. AWS: Assume Role 用の IAM ロールを作成

- Terraform の実行権限
- IAM ポリシーとして AdministratorAccess を付与
- 信頼関係として前項で作成した IAM ユーザを Principal に設定する
- また、信頼関係で`aws:MultiFactorAuthPresent`を`true`に設定し、多要素認証を強制する
- 最大セッション期間を適宜修正する(`get-credential.sh`では 8 時間を想定しているため、合わせて修正する)

3. ローカル: `aws configure`で前項で作成した IAM ユーザを設定

- default でない場合は`export AWS_DEFAULT_PROFILE=[プロフィール名]`を実行する

4. ローカル: .env ファイルを作成

- 以下を記載する
  ```.env
  PYTHONPATH=devfrapy/src
  EXEC_TF_ROLE_ARN=[Assume Role用IAMロールのARN]
  ASSUME_ROLE_MFA_ARN=[ローカル実行用IAMユーザのMFAデバイスのARN]
  ASSUME_ROLE_AWS_ACCESS_KEY_ID=[ローカル実行用IAMユーザのアクセスキー]
  ASSUME_ROLE_AWS_SECRET_ACCESS_KEY=[ローカル実行用IAMユーザのシークレットアクセスキー]
  ASSUME_ROLE_AWS_REGION=[実行対象のリージョン]
  ```

5. Terraform 環境で example を実行する

```shell
./scripts.sh docker_up
./scripts.sh docker_exec

# dockerコンテナ上での操作
source ./scripts.sh get_credentials `[ワンタイムパスワード]`
cd example
python ../devfrapy/src/main.py config/basic.yml .
terraform init
terraform plan -var-file config/tfvar.json
terraform apply -var-file config/tfvar.json

# AWSリソースの作成確認後
terraform destroy -var-file config/tfvar.json
rm secret.json
```
