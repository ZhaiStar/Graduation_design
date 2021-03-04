from alipay import AliPay


def Pay(order, money, id):
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk2WG3ch2Yp+wBIw4Hon59GChacfhyjkZltvg43zdVFQj0Je4ifO9Xp+Te9l4xZL27kmtjt7svdvuHfhSGXancMcQXOQpvhX+d812S8CMj+OKtb6Axcy8ZbhNCNPXgf28qd+bAJrNUeplggMkqEOFSTi+1uEqP2Xd15ihmEyzYbQHHjCzDloCUzaOmlb9mBgUaECzGqpgZpkgNlyx6PXAPdh7NxplBaH9iw3YF9EYGWl2VPBmJg9Y1r6L4CQeQn7YCsppB4QbIh0BgoKV7k9LXWFP5k0QcrtDBQVemCDgjSOJZJMKIWvtunLO4OFwZNB+26UugmCuwgXJx10R+fGAWQIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAk2WG3ch2Yp+wBIw4Hon59GChacfhyjkZltvg43zdVFQj0Je4ifO9Xp+Te9l4xZL27kmtjt7svdvuHfhSGXancMcQXOQpvhX+d812S8CMj+OKtb6Axcy8ZbhNCNPXgf28qd+bAJrNUeplggMkqEOFSTi+1uEqP2Xd15ihmEyzYbQHHjCzDloCUzaOmlb9mBgUaECzGqpgZpkgNlyx6PXAPdh7NxplBaH9iw3YF9EYGWl2VPBmJg9Y1r6L4CQeQn7YCsppB4QbIh0BgoKV7k9LXWFP5k0QcrtDBQVemCDgjSOJZJMKIWvtunLO4OFwZNB+26UugmCuwgXJx10R+fGAWQIDAQABAoIBAG8haSHmdnu9cnS7U8SSuwZppMmgjrhtfMGlXlWmWymtlqM7AUPhpbGmFwiV2tz8BXl7y4OgyFYNb+bgxuWz9GKvc8LVtDNBWe7x1nMe5dvG71pAG88GojT/U/WH40B7Erfxg2hdTtioJYh03jqPTfr68cgJVFUgdLaMuameitDqSaQpuLGMlbfIRf/JaXesrm7Ti28mkqa8gg3tHi2yBYuYcAu/CknqEFZU3SVppyayK1VRzaxyuUTq9Oc87fVWiww8KmirGC6ZQZFIE7Ts2QRn28Tk6jgpcgaBwD/M0ad17ZSQY2u+m9HozSCx4Vo+wsqYcbdbCpNw0hiaJ9YGpgECgYEA0DNO/49EBAVInOFx3AVOseMbxUpY+NNPkIdukQkdxhYWYwyiZyW7MHlqbtfN2lFAl7f6354+77vp5d1ITiDDWBAXqOoLFKf8eoaUvKbXz/EMNze7bvTxWwbwd+NCkeNY4zAVAp3L0IJLqD+kHbOpFEHTIPSlq+qeMUIJeuFL4PECgYEAtTyOnYh3lcr3TVdp7BRxm+gW+F5uSLtPJw6y4Pf3C8MXxKCudrr4V6V0TxBv7yzO0IYNsc+JbEcDLztyEw6/NRxg23yg1MXYE4o1prqVhX0H+4pcarvWVEDgFTkkbcShhysyqERtp3br/Vx2cpsadW6tfqTasAmPJj4uQ7lOFekCgYEAkrgVq7LiU5MFoMie3FZBJsrM/zNtj6waHdfS6xJpkPZvwE1fBSFp0Lc/ce1Se89WnZRhjsSNxZO/OOW/1o7wGlb81WRZeq0HF7FPj8Jjw34zBZaY15B1pZg2TcYxW23DbhasN7PLtZychGyU0vmQ5V2d01OUjJpB8KSA2b97IYECgYBbjqAtjUd8cPDGLabhEOLj9DfGeU4ViCrQfGh5pkszsfdL6jC44nObM4ayeodRuL0yMsawUTwHa0h8j/dtEUIfPprfxvIpC1nBZUz9Ub0/lo510MwnT4VTQwLxNdDlczR26KfKwebzdux5LkDYXOrc8HDNTdL8o5ehpkARDogYIQKBgQC6FRkhb7IDA2eLeEJZhZl5A8BOxHO8LsPtzu/raMFttNUsQRovfg/iBS3bPHh3jGVRWIrbVmjohEeuCwCd5DADXx712TomaDQXkxKShdhAhm0Er3wVU0aarnmJzg7VOjex50h4BBqv7CWzbf2TQphBN9OHW2cd80ODbyssp6ATww==
    -----END RSA PRIVATE KEY-----'''

    alipay = AliPay(
        appid="2016101500695640",  # 支付宝app的id
        app_notify_url="",  # 回调视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url=f"http://127.0.0.1:8000/user/pay_result/?order_id={id}",  # 完成之后返回
        notify_url=f"http://127.0.0.1:8000/user/pay_result/?order_id={id}"  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string


if __name__ == '__main__':
    print(Pay("15730481663917723", "1000"))
