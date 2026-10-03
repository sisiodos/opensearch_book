import java.nio.file.*;
import java.util.*;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.search.*;
import org.apache.lucene.store.*;
public class LuceneProbe {
 static void check(boolean b,String m) { if(!b)throw new AssertionError(m); }
 static Document doc(String id,int value) {
  Document d=new Document();d.add(new StringField("id",id,Field.Store.YES));d.add(new TextField("text","OpenSearch Lucene",Field.Store.NO));d.add(new StringField("keyword","OpenSearch Lucene",Field.Store.NO));d.add(new IntPoint("numeric",value));d.add(new NumericDocValuesField("numeric",value));d.add(new SortedDocValuesField("keyword",new org.apache.lucene.util.BytesRef("OpenSearch Lucene")));d.add(new LatLonPoint("geo",35.68,139.76));d.add(new LatLonDocValuesField("geo",35.68,139.76));d.add(new StoredField("source","{\"id\":\""+id+"\"}"));return d;
 }
 public static void main(String[] args)throws Exception {
  Path path=Files.createTempDirectory("lucene-book-probe-");
  try(Directory dir=FSDirectory.open(path)) {
   IndexWriterConfig conf=new IndexWriterConfig(new StandardAnalyzer());conf.setMergePolicy(NoMergePolicy.INSTANCE);
   try(IndexWriter w=new IndexWriter(dir,conf)) {w.addDocument(doc("removed",1));w.addDocument(doc("kept",2));w.commit();}
   int before;
   try(DirectoryReader r=DirectoryReader.open(dir)) {
    before=new IndexSearcher(r).search(new TermQuery(new Term("id","kept")),1).scoreDocs[0].doc;
    LeafReader leaf=r.leaves().get(0).reader();
    for(FieldInfo f:leaf.getFieldInfos()) System.out.println("FIELD "+f.name+" index="+f.getIndexOptions()+" docValues="+f.getDocValuesType()+" pointDimensions="+f.getPointDimensionCount());
    check(leaf.getFieldInfos().fieldInfo("numeric").getPointDimensionCount()==1,"numeric points");
    check(leaf.getFieldInfos().fieldInfo("geo").getPointDimensionCount()==2,"geo points");
    check(leaf.getFieldInfos().fieldInfo("keyword").getDocValuesType()==DocValuesType.SORTED,"keyword docvalues");
    check(leaf.getFieldInfos().fieldInfo("text").getDocValuesType()==DocValuesType.NONE,"text no docvalues");
    Terms terms=leaf.terms("text");TermsEnum te=terms.iterator();check(te.seekExact(new org.apache.lucene.util.BytesRef("lucene")),"lucene term");PostingsEnum pe=te.postings(null,PostingsEnum.ALL);
    while(pe.nextDoc()!=DocIdSetIterator.NO_MORE_DOCS)System.out.println("POSTING lucene docID="+pe.docID()+" frequency="+pe.freq());
    System.out.println("SOURCE "+r.storedFields().document(before).get("source"));
   }
   IndexWriterConfig merge=new IndexWriterConfig(new StandardAnalyzer());
   try(IndexWriter w=new IndexWriter(dir,merge)) {w.deleteDocuments(new Term("id","removed"));w.forceMerge(1);w.commit();}
   try(DirectoryReader r=DirectoryReader.open(dir)) {
    int after=new IndexSearcher(r).search(new TermQuery(new Term("id","kept")),1).scoreDocs[0].doc;
    check(before!=after,"docID changes after deletion and merge");check(r.storedFields().document(after).get("id").equals("kept"),"stored identifier unchanged");System.out.println("DOCID kept before="+before+" after="+after);System.out.println("PASS Lucene index probe");
   }
  }
 }
}
