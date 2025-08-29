import torch
import torch.nn as nn
import torch.nn.functional as F

class model_class(nn.Module):
    def __init__(self,input_size=27,hidden_size=256,output_size=50):
        super().__init__()
        self.input_size=input_size
        self.hidden_size=hidden_size
        self.output_size=output_size
        self.encoder=nn.LSTM(self.input_size,self.hidden_size,2,bidirectional=True)
        self.u=nn.Linear(self.hidden_size*2,self.hidden_size)
        self.w1=nn.Linear(self.hidden_size,self.hidden_size)
        self.w2=nn.Linear(self.hidden_size,self.hidden_size)
        self.w3=nn.Linear(self.hidden_size,self.hidden_size)
        self.w4=nn.Linear(self.hidden_size,self.hidden_size)
        self.w=nn.Linear(self.hidden_size,self.hidden_size)
        self.atten=nn.Linear(self.hidden_size,1)
        self.output2catin=nn.Linear(self.output_size,self.hidden_size*2)
        self.decoder=nn.LSTM(self.hidden_size*4,self.hidden_size,4)
        self.hidden_output=nn.Linear(self.hidden_size,self.output_size)
        self.softmax=nn.LogSoftmax(dim=2)
    def forward_pass(self,inputs,max_chars=30,ground_truth=None):
        enc_outputsw,enc_hidden=self.encoder(inputs) #(n,1,512)
        decoder_state1=enc_hidden[0] # consider only the hidden state of 4*1*256
        decoder_state2=torch.zeros(4,1,self.hidden_size)
        decoder_input=torch.zeros(1,1,self.output_size)
        enc_outputs=enc_outputsw.view(-1,self.hidden_size*2) #(n,512)
        u=self.u(enc_outputs) #(n,256)
        outputs=[]
        for i in range(max_chars):
            w1=self.w1(decoder_state1[0].view(1,-1).repeat(enc_outputs.shape[0],1)) # (n,256)
            w2=self.w2(decoder_state1[1].view(1,-1).repeat(enc_outputs.shape[0],1))
            w3=self.w3(decoder_state1[2].view(1,-1).repeat(enc_outputs.shape[0],1))
            w4=self.w4(decoder_state1[3].view(1,-1).repeat(enc_outputs.shape[0],1))
            w=self.w(w1+w2+w3+w4) #(7,256)
            v=self.atten(torch.tanh(u+w)) #(n,256) -> (n,1)
            alpha=F.softmax(v.view(1,-1),dim=1)
            cj=torch.bmm(alpha.unsqueeze(0),enc_outputs.unsqueeze(0)) # 1,7,1 1,7,512, 1,1,512
            ins=self.output2catin(decoder_input)
            decoder_input=torch.cat((ins[0],cj[0]),1).unsqueeze(0)
            decoder_output,decoder_state=self.decoder(decoder_input,(decoder_state1,decoder_state2))
            out=self.hidden_output(decoder_output)
            output=self.softmax(out)
            outputs.append(output.view(1,-1))
            max_index=torch.argmax(output,1,keepdim=True)
            if ground_truth is not None:
                max_index=ground_truth[i].reshape(1,1,1)
            one_hot=torch.zeros(output.shape)
            one_hot.scatter_(2,max_index,1)
            decoder_input=one_hot.detach()
            decoder_state1=decoder_state[0]
            decoder_state2=decoder_state[1]
        return outputs