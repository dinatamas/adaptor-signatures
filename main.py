#!/usr/bin/env python3
#
# Elliptic curve crypto and MuSig demo.
#
from pprint import pprint

from elliptic_curve.secp256k1 import generate_key_pair
from protocol.musig import MuSigSession, sum_musig_signatures


if __name__ == '__main__':
    # The message Alice and Bob want to sign.
    msg = 'Hello'.encode()

    # These will store Alice's and Bob's data.
    adata = MuSigSession()
    bdata = MuSigSession()

    # 1. Generate permanent keys.
    adata.x, adata.X = generate_key_pair()
    bdata.x, bdata.X = generate_key_pair()

    # 2. Generate temporary keys (private / public nonces).
    adata.r, adata.R = generate_key_pair()
    bdata.r, bdata.R = generate_key_pair()

    # 3. Transfer permanent public keys.
    adata.Xs = bdata.Xs = [adata.X, bdata.X]

    # 4. Transfer commitments.
    adata.ts = bdata.ts = [adata.t, bdata.t]

    # 5. Transfer temporary public keys.
    adata.Rs = bdata.Rs = [adata.R, bdata.R]

    # 6. Prepare individual signatures.
    alice_sign = adata.sign(msg)
    bob_sign = bdata.sign(msg)

    # Verify own signatures.
    assert not adata.verify(msg, alice_sign)
    assert not bdata.verify(msg, bob_sign)

    # Verify each others' signatures.
    assert not adata.verify(msg, bob_sign)
    assert not bdata.verify(msg, alice_sign)

    # 7. Verify common (aggregated) signature.
    common_sign = sum_musig_signatures((alice_sign, bob_sign))
    assert adata.verify(msg, common_sign)
    assert bdata.verify(msg, common_sign)

    print('All working correctly!')
    # TODO: dataclass should also print cached properties!
    pprint(adata)
    pprint(bdata)
