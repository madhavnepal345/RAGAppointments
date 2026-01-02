from typing import List,Optional
import re
import tiktoken

class Chunker:
    def __init__(self,chunk_size:int=1000,chunk_overlap:int=200):
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        self.tokenizer=tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self,text:str)->int:
        return len(self.tokenizer.encode(text))
    

    def recursive_chunking(self,text:str)->List[str]:
        paragraphs=[p for p in text.split('\n\n') if p.strip()]
        chunks=[]
        current_chunk=[]
        current_tokens=0

        for paragraph in paragraphs:
            paragraph_tokens=self._count_tokens(paragraph)
            if current_tokens + paragraph_tokens > self.chunk_size and current_chunk:
                chunks.append('\n\n'.join(current_chunk))

                if self.chunk_overlap>0 and current_chunk:
                    overlap_text=('\n\n'.join(current_chunk[-2:]) if len(current_chunk)>=2 else current_chunk[-1])
                    overlap_tokens=self._count_tokens(overlap_text)

                    if overlap_tokens>self.chunk_overlap:
                        current_chunk=[overlap_text,paragraph]
                        current_tokens=overlap_tokens+paragraph_tokens
                    else:
                        current_chunk=[paragraph]
                        current_tokens=paragraph_tokens
                else:
                    current_chunk=[paragraph]
                    current_tokens=paragraph_tokens
            else:
                current_chunk.append(paragraph)
                current_tokens+=paragraph_tokens
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
def semantic_chunking(self,text:str)->List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences=[s.strip()for s in sentences if s.strip()]

    chunks=[]
    current_chunk=[]
    current_tokens=0


    for sentence in sentences:
        sentence_tokens=self._count_tokens(sentence)
        if current_tokens + sentence_tokens>self.chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))

            #handaling overlap
            if self.chun_overlap >0 and current_chunk:
                overlap_sentences=[]
                overlap_tokens=0

                for s in reversed(current_chunk):
                    s_tokens=self._count_tokens(s)
                    if overlap_tokens + s_tokens <=self.chunk_overlap:
                        overlap_sentences.insert(0,s)
                        overlap_tokens+=s_tokens
                    else:
                        break
                current_chunk=overlap_sentences+[sentence]
                current_tokens=overlap_tokens + sentence_tokens
            else:
                current_chunk=[sentence]
                current_tokens=sentence_tokens
        else:
            current_chunk.append(sentence)
            current_tokens+=sentence_tokens
    if current_chunk:
        chunks.append(' '.join(current_chunk))


    return chunks


def chunk_text(self,text:str,strategy:str='recursive')->List[str]:
    if strategy=='recursive':
        return self.recursive_chunking(text)
    elif strategy=='semantic':
        return self.semantic_chunking(text)
    else:
        raise ValueError("Unsupported chunking strategy")

