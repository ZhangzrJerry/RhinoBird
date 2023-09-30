# import paddle
# import paddle.nn as nn
#
#
# class DSSM(nn.Layer):
#     def __init__(self, len_users, len_items):
#         super(DSSM, self).__init__()
#         self.users_emb = nn.Embedding(len_users + 1, 256)
#         self.items_emb = nn.Embedding(len_items + 1, 256)
#         self.user_fc1 = nn.Linear(256, 128)
#         self.item_fc1 = nn.Linear(256, 128)
#         self.relu = nn.ReLU()
#         self.sigmoid = nn.Sigmoid()
#         self.cos = nn.CosineSimilarity()
#         pass
#
#     def forward(self, input):
#         user = self.users_emb(input[:, 0])
#         item = self.items_emb(input[:, 1])
#         user = self.user_fc1(user)
#         item = self.item_fc1(item)
#         user = self.relu(user)
#         item = self.relu(item)
#         x = self.cos(user, item)
#         x = self.sigmoid(x)
#         return x
#
#     pass