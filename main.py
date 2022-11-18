#!/usr/bin/env python3
#
# Elliptic curve crypto and MuSig demo.
#
from elliptic_curve.secp256k1 import generate_key_pair
from protocol.musig import sign_message, verify_signature
from protocol.utils import p2b, sha256


if __name__ == '__main__':
    # Alice wants to get M1 signed by Bob.
    # Bob wants to get M2 signed by Alice.
    M1 = 'Transfer 100 USD from Bob to Alice'.encode()
    M2 = 'Transfer 100 EUR from Alice to Bob'.encode()

    # Generate permanent private and public keys.
    xA, XA = generate_key_pair()
    xB, XB = generate_key_pair()

    # Step #1 and #2: M1, M2, XA, XB are exchanged.
    # The list of permanent public keys.
    # All signing parties must use the same order.
    Xs = sorted((XA, XB))
    
    # Generate temporary (nonce) private and public keys.
    rA1, RA1 = generate_key_pair()
    rA2, RA2 = generate_key_pair()
    rB1, RB1 = generate_key_pair()
    rB2, RB2 = generate_key_pair()

    # Hash the public nonces.
    TA1 = sha256(p2b(RA1))
    TA2 = sha256(p2b(RA2))
    TB1 = sha256(p2b(RB1))
    TB2 = sha256(p2b(RB2))

    # Step #3: TA1, TA2, TB1, TB2 are exchanged.
    # Step #4: RA1, RA2, RB1, RB2 are exchanged.
    # The list of nonce public keys.
    # All signing parties must use the same order.
    R1s = sorted((RA1, RB1))
    R2s = sorted((RA2, RB2))

    # Alice verifies.
    assert sha256(p2b(RB1)) == TB1
    assert sha256(p2b(RB2)) == TB2
    # Bob verifies.
    assert sha256(p2b(RA1)) == TA1
    assert sha256(p2b(RA2)) == TA2

    # Alice produces the adaptor signatures.
    o, O = generate_key_pair()
    sA1 = sign_message(M1, xA, XA, Xs, rA1, RA1, R1s)
    SA1 = sA1 + o
    sA2 = sign_message(M2, xA, XA, Xs, rA2, RA2, R2s)
    SA2 = sA2 + o

    # Step #5: O, SA1, SA2 are exchanged.

    # Bob also produces his signatures.
    sB1 = sign_message(M1, xB, XB, Xs, rB1, RB1, R1s)
    sB2 = sign_message(M2, xB, XB, Xs, rB2, RB2, R2s)

    # Bob verifies that the offset signatures are valid.
    assert verify_signature(M1, sB1 + SA1, Xs, R1s, offset=O)
    assert verify_signature(M2, sB2 + SA2, Xs, R2s, offset=O)

    # Step #6: Bob transmits sB1 to Alice.

    # Step #7: Alice calculates (and reveals) sC1.
    sC1 = sA1 + sB1

    # From sC1 Bob can recover Alice's signatures, and thus calculate sC2.
    o = -(sC1 - SA1 - sB1)
    sA1 = SA1 - o
    sA2 = SA2 - o
    sC2 = sA2 + sB2

    # Sanity check: the common signatures are valid.
    assert verify_signature(M1, sC1, Xs, R1s)
    assert verify_signature(M2, sC2, Xs, R2s)
    print('Everything works as expected! :^)')
