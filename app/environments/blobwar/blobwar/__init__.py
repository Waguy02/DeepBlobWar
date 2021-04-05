from gym.envs.registration import register

register(
    id='BlobWar-v0',
    entry_point='blobwar.envs:BlobWarEnv',
)


