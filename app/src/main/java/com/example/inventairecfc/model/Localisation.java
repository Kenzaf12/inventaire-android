package com.example.inventairecfc.model;

public class Localisation {
    private Long id;
    private String site;
    private String etage;
    private Integer nlocal;
    private String typeLocal;
    private String appartenance;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getSite() { return site; }
    public void setSite(String site) { this.site = site; }
    public String getEtage() { return etage; }
    public void setEtage(String etage) { this.etage = etage; }
    public Integer getNlocal() { return nlocal; }
    public void setNlocal(Integer nlocal) { this.nlocal = nlocal; }
    public String getTypeLocal() { return typeLocal; }
    public void setTypeLocal(String typeLocal) { this.typeLocal = typeLocal; }
    public String getAppartenance() { return appartenance; }
    public void setAppartenance(String appartenance) { this.appartenance = appartenance; }
}
