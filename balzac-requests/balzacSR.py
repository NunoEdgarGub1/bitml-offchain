import requests

urlPutCode = 'http://localhost:8080/balzac/xtext-service/update?resource=9b8085f.balzac'
urlGetResult = 'http://localhost:8080/balzac/xtext-service/generate?resource=9b8085f.balzac&requiredStateId=-80000000'
code = {'fullText': '''/*
 * Oracle
 *
 * https://blockchain.unica.it/balzac/docs/oracle.html
 */

// tx with Alice's funds, redeemable with Alice's private key
transaction A_funds {
    input = _
    output = 1 BTC: fun(x). versig(Alice.kApub; x)
}

participant Alice {
    // Alice's private key
    private const kA = key:cSthBXr8YQAexpKeh22LB9PdextVE1UJeahmyns5LzcmMDSy59L4
    // Alice's public key
    const kApub = kA.toPubkey

    transaction T {
        input = A_funds: sig(kA)
        output = 1 BTC: fun(sigB, sigO). versig(Bob.kBpub, Oracle.kOpub; sigB, sigO)
    }
}

participant Bob {
    // Bob's private key
    private const kB = key:cQmSz3Tj3usor9byskhpCTfrmCM5cLetLU9Xw6y2csYhxSbKDzUn
    // Bob's public key
    const kBpub = kB.toPubkey

    transaction T1(sigO) {
        input = Alice.T: sig(kB) sigO
        output = 1 BTC: fun(x). versig(kB; x)
    }
}

participant Oracle {
    // Oracle's private key
    private const kO = key:cTyxEAoUSKcC9NKFCjxKTaXzP8i1ufEKtwVVtY6AsRPpRgJTZQRt
    // Oracle's public key
    const kOpub = kO.toPubkey

    const sigO = sig(kO) of Bob.T1(_)
}


eval Alice.T, Bob.T1(Oracle.sigO)
 '''}
cook = requests.Session()
cook.put(urlPutCode, data=code)
response = cook.get(urlGetResult)

print(response.content)


