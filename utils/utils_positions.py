# -*- coding: utf-8 -*-

# Funzioni di utilità per i movimenti del robot NAO.
# Tutte le funzioni accettano l'istanza 'nao' come primo parametro.

def head(nao, yaw, pitch, duration):
    nao.motion.angleInterpolation(
        ["HeadYaw", "HeadPitch"],
        [yaw, pitch],
        [duration, duration],
        True
    )

def arms_both(nao, l_pitch, l_roll, r_pitch, r_roll, duration):
    nao.motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll"],
        [l_pitch, l_roll, r_pitch, r_roll],
        [duration, duration, duration, duration],
        True
    )

def right_arm_magic_pose(nao, duration):
    nao.motion.angleInterpolation(
        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"],
        [0.95, -0.22, 1.0, 0.65, 0.15, 1.0],
        [duration, duration, duration, duration, duration, duration],
        True
    )

def open_arms_small(nao, duration):
    # Nota: ho rimosso yaw e pitch come parametri extra se non usati coerentemente
    nao.motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll"],
        [1.10, 0.22, 1.10, -0.22],
        [duration, duration, duration, duration],
        True
    )

def close_arms(nao, duration):
    nao.motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll", "RHand", "LHand"],
        [1.45, 0.15, 1.45, -0.15, 0.0, 0.0],
        [duration, duration, duration, duration, duration, duration],
        True
    )

def indicate_jury(nao, duration):
    nao.motion.angleInterpolation(
        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand"],
        [0.75, -0.42, 0.65, 0.45, 1.0],
        [duration, duration, duration, duration, duration],
        True
    )

def close_right_hand(nao, duration):
    nao.motion.angleInterpolation(
        ["RHand"],
        [0.0],
        [duration],
        True
    )

def pour_motion(nao, duration):
    nao.motion.angleInterpolation(
        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"],
        [0.95, -0.15, 0.9, 0.6, -0.45, 1.0],
        [duration, duration, duration, duration, duration, duration],
        True
    )

def arms_sad(nao, duration):
    nao.motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll", "RHand", "LHand"],
        [1.55, 0.10, 1.55, -0.10, 0.0, 0.0],
        [duration, duration, duration, duration, duration, duration],
        True
    )

def arms_open_happy(nao, duration):
    nao.motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll", "RHand", "LHand"],
        [0.95, 0.55, 0.95, -0.55, 0.0, 0.0],
        [duration, duration, duration, duration, duration, duration],
        True
    )

def final_pose(nao, duration):
    nao.motion.angleInterpolation(
        ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll", "RHand", "LHand"],
        [1.0, 0.35, 1.0, -0.35, 0.0, 0.0],
        [duration, duration, duration, duration, duration, duration],
        True
    )
    
