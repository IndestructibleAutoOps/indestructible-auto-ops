// @GL-governed
// @GL-layer: GL-L8-DOC
// @GL-semantic: governance-layer-documentation
// @GL-revision: 1.0.0
// @GL-status: active

// MachineNativeOps Interactive DAG Visualization
// Using D3.js for rendering

class DAGVisualization {
    constructor(containerId) {
        this.container = d3.select(containerId);
        this.width = this.container.node().getBoundingClientRect().width || 800;
        this.height = 600;
        this.nodes = getNodes();
        this.links = getLinks();
        this.selectedNode = null;
        this.currentLayout = 'hierarchical';
        
        this.nodeWidth = 140;
        this.nodeHeight = 60;
        
        this.init();
    }
    
    init() {
        // Clear existing content
        this.container.selectAll("*").remove();
        
        // Create SVG
        this.svg = this.container
            .attr("width", this.width)
            .attr("height", this.height);
        
        // Add definitions for gradients and arrows
        this.addDefs();
        
        // Create zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([0.3, 3])
            .on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            });
        
        this.svg.call(this.zoom);
        
        // Create main group for zoom/pan
        this.g = this.svg.append("g")
            .attr("class", "graph-group");
        
        // Create tooltip
        this.tooltip = d3.select("body").append("div")
            .attr("class", "tooltip");
        
        // Render the graph
        this.render();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Update statistics
        this.updateStatistics();
    }
    
    addDefs() {
        const defs = this.svg.append("defs");
        
        // Gradient for active modules
        const gradientActive = defs.append("linearGradient")
            .attr("id", "gradient-active")
            .attr("x1", "0%").attr("y1", "0%")
            .attr("x2", "100%").attr("y2", "100%");
        gradientActive.append("stop").attr("offset", "0%").attr("stop-color", "#10b981");
        gradientActive.append("stop").attr("offset", "100%").attr("stop-color", "#059669");
        
        // Gradient for in-development modules
        const gradientDev = defs.append("linearGradient")
            .attr("id", "gradient-dev")
            .attr("x1", "0%").attr("y1", "0%")
            .attr("x2", "100%").attr("y2", "100%");
        gradientDev.append("stop").attr("offset", "0%").attr("stop-color", "#f59e0b");
        gradientDev.append("stop").attr("offset", "100%").attr("stop-color", "#d97706");
        
        // Gradient for global layer
        const gradientGlobal = defs.append("linearGradient")
            .attr("id", "gradient-global")
            .attr("x1", "0%").attr("y1", "0%")
            .attr("x2", "100%").attr("y2", "100%");
        gradientGlobal.append("stop").attr("offset", "0%").attr("stop-color", "#8b5cf6");
        gradientGlobal.append("stop").attr("offset", "100%").attr("stop-color", "#7c3aed");
        
        // Arrow marker
        defs.append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "-0 -5 10 10")
            .attr("refX", 8)
            .attr("refY", 0)
            .attr("orient", "auto")
            .attr("markerWidth", 8)
            .attr("markerHeight", 8)
            .append("path")
            .attr("d", "M 0,-5 L 10,0 L 0,5")
            .attr("class", "link-arrow");
    }
    
    render() {
        // Calculate positions based on layout
        this.calculatePositions();
        
        // Render links first (so they appear behind nodes)
        this.renderLinks();
        
        // Render nodes
        this.renderNodes();
        
        // Center the graph
        this.centerGraph();
    }
    
    calculatePositions() {
        switch (this.currentLayout) {
            case 'hierarchical':
                this.calculateHierarchicalPositions();
                break;
            case 'force':
                this.calculateForcePositions();
                break;
            case 'radial':
                this.calculateRadialPositions();
                break;
            default:
                this.calculateHierarchicalPositions();
        }
    }
    
    calculateHierarchicalPositions() {
        const levelHeight = 120;
        const levelWidth = 200;
        
        // Group nodes by depth
        const levels = {};
        this.nodes.forEach(node => {
            const depth = node.depth;
            if (!levels[depth]) levels[depth] = [];
            levels[depth].push(node);
        });
        
        // Position nodes
        Object.entries(levels).forEach(([depth, nodesAtLevel]) => {
            const y = parseInt(depth) * levelHeight + 80;
            const totalWidth = nodesAtLevel.length * levelWidth;
            const startX = (this.width - totalWidth) / 2 + levelWidth / 2;
            
            nodesAtLevel.forEach((node, i) => {
                node.x = startX + i * levelWidth;
                node.y = y;
            });
        });
    }
    
    calculateForcePositions() {
        // Use D3 force simulation
        const simulation = d3.forceSimulation(this.nodes)
            .force("link", d3.forceLink(this.links).id(d => d.id).distance(150))
            .force("charge", d3.forceManyBody().strength(-500))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("collision", d3.forceCollide().radius(80))
            .stop();
        
        // Run simulation
        for (let i = 0; i < 300; i++) simulation.tick();
    }
    
    calculateRadialPositions() {
        const centerX = this.width / 2;
        const centerY = this.height / 2;
        const maxRadius = Math.min(this.width, this.height) / 2 - 100;
        
        // Group nodes by depth
        const levels = {};
        let maxDepth = 0;
        this.nodes.forEach(node => {
            const depth = node.depth;
            if (!levels[depth]) levels[depth] = [];
            levels[depth].push(node);
            maxDepth = Math.max(maxDepth, depth);
        });
        
        // Position nodes in concentric circles
        Object.entries(levels).forEach(([depth, nodesAtLevel]) => {
            const radius = (parseInt(depth) / maxDepth) * maxRadius + 50;
            const angleStep = (2 * Math.PI) / nodesAtLevel.length;
            const startAngle = -Math.PI / 2;
            
            nodesAtLevel.forEach((node, i) => {
                const angle = startAngle + i * angleStep;
                node.x = centerX + radius * Math.cos(angle);
                node.y = centerY + radius * Math.sin(angle);
            });
        });
    }
    
    renderLinks() {
        // Remove existing links
        this.g.selectAll(".link").remove();
        
        // Create link elements
        const linkData = this.links.map(link => {
            const source = this.nodes.find(n => n.id === link.source || n.id === link.source.id);
            const target = this.nodes.find(n => n.id === link.target || n.id === link.target.id);
            return { source, target };
        });
        
        this.linkElements = this.g.selectAll(".link")
            .data(linkData)
            .enter()
            .append("path")
            .attr("class", "link")
            .attr("marker-end", "url(#arrowhead)")
            .attr("d", d => this.getLinkPath(d.source, d.target));
    }
    
    getLinkPath(source, target) {
        const sourceX = source.x;
        const sourceY = source.y + this.nodeHeight / 2;
        const targetX = target.x;
        const targetY = target.y - this.nodeHeight / 2 - 10;
        
        // Create curved path
        const midY = (sourceY + targetY) / 2;
        
        return `M ${sourceX} ${sourceY} 
                C ${sourceX} ${midY}, ${targetX} ${midY}, ${targetX} ${targetY}`;
    }
    
    renderNodes() {
        // Remove existing nodes
        this.g.selectAll(".node").remove();
        
        // Create node groups
        const nodeGroups = this.g.selectAll(".node")
            .data(this.nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.x - this.nodeWidth/2}, ${d.y - this.nodeHeight/2})`)
            .on("click", (event, d) => this.onNodeClick(d))
            .on("mouseover", (event, d) => this.onNodeHover(event, d))
            .on("mouseout", () => this.onNodeOut());
        
        // Add rectangles
        nodeGroups.append("rect")
            .attr("class", d => `node-rect ${this.getNodeClass(d)}`)
            .attr("width", this.nodeWidth)
            .attr("height", this.nodeHeight)
            .attr("rx", 8)
            .attr("ry", 8);
        
        // Add module ID text
        nodeGroups.append("text")
            .attr("class", "node-text")
            .attr("x", this.nodeWidth / 2)
            .attr("y", this.nodeHeight / 2 - 6)
            .text(d => d.id);
        
        // Add autonomy level text
        nodeGroups.append("text")
            .attr("class", "node-text node-subtext")
            .attr("x", this.nodeWidth / 2)
            .attr("y", this.nodeHeight / 2 + 12)
            .text(d => d.autonomyLevel);
        
        this.nodeElements = nodeGroups;
    }
    
    getNodeClass(node) {
        if (node.autonomyLevel === "Global Layer") return "global-layer";
        if (node.status === "in-development") return "in-development";
        return "active";
    }
    
    onNodeClick(node) {
        // Deselect previous
        this.nodeElements.selectAll(".node-rect").classed("selected", false);
        
        // Select current
        this.selectedNode = node;
        this.nodeElements.filter(d => d.id === node.id)
            .select(".node-rect")
            .classed("selected", true);
        
        // Highlight connected links
        this.highlightConnections(node);
        
        // Update info panel
        this.updateInfoPanel(node);
    }
    
    highlightConnections(node) {
        // Reset all links
        this.linkElements.classed("highlighted", false);
        
        // Highlight links connected to this node
        this.linkElements.classed("highlighted", d => 
            d.source.id === node.id || d.target.id === node.id
        );
    }
    
    onNodeHover(event, node) {
        this.tooltip
            .classed("visible", true)
            .html(`
                <h4>${node.id}</h4>
                <p><strong>${node.name}</strong></p>
                <p>Autonomy: ${node.autonomyLevel}</p>
                <p>Health: ${node.semanticHealth}%</p>
                <p>Status: ${node.status}</p>
            `)
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 10) + "px");
    }
    
    onNodeOut() {
        this.tooltip.classed("visible", false);
    }
    
    updateInfoPanel(node) {
        document.querySelector(".hint").classList.add("hidden");
        document.getElementById("module-details").classList.remove("hidden");
        
        document.getElementById("detail-id").textContent = node.id;
        document.getElementById("detail-name").textContent = node.name;
        document.getElementById("detail-autonomy").textContent = node.autonomyLevel;
        document.getElementById("detail-status").textContent = node.status;
        document.getElementById("detail-health").textContent = node.semanticHealth + "%";
        document.getElementById("detail-deps").textContent = node.dependencies.length > 0 
            ? node.dependencies.join(", ") 
            : "None";
        document.getElementById("detail-dependents").textContent = node.dependents.length > 0 
            ? node.dependents.join(", ") 
            : "None";
        document.getElementById("detail-namespace").textContent = node.namespace;
    }
    
    updateStatistics() {
        const stats = moduleData.statistics;
        document.getElementById("stat-modules").textContent = stats.totalModules;
        document.getElementById("stat-deps").textContent = stats.totalDependencies;
        document.getElementById("stat-depth").textContent = stats.maxDepth;
        document.getElementById("stat-cycles").textContent = stats.cycles === 0 ? "0 ✅" : stats.cycles + " ⚠️";
    }
    
    centerGraph() {
        // Calculate bounds
        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
        this.nodes.forEach(node => {
            minX = Math.min(minX, node.x - this.nodeWidth/2);
            maxX = Math.max(maxX, node.x + this.nodeWidth/2);
            minY = Math.min(minY, node.y - this.nodeHeight/2);
            maxY = Math.max(maxY, node.y + this.nodeHeight/2);
        });
        
        const graphWidth = maxX - minX;
        const graphHeight = maxY - minY;
        
        // Calculate scale and translation
        const scale = Math.min(
            (this.width - 40) / graphWidth,
            (this.height - 40) / graphHeight,
            1
        );
        
        const translateX = (this.width - graphWidth * scale) / 2 - minX * scale;
        const translateY = (this.height - graphHeight * scale) / 2 - minY * scale;
        
        // Apply transform
        this.svg.call(
            this.zoom.transform,
            d3.zoomIdentity.translate(translateX, translateY).scale(scale)
        );
    }
    
    setLayout(layout) {
        this.currentLayout = layout;
        this.render();
    }
    
    filterByStatus(status) {
        if (status === 'all') {
            this.nodes = getNodes();
        } else {
            this.nodes = getNodes().filter(n => n.status === status);
        }
        this.links = getLinks().filter(link => 
            this.nodes.some(n => n.id === link.source) && 
            this.nodes.some(n => n.id === link.target)
        );
        this.render();
    }
    
    resetZoom() {
        this.centerGraph();
    }
    
    exportSVG() {
        const svgElement = this.svg.node();
        const serializer = new XMLSerializer();
        let svgString = serializer.serializeToString(svgElement);
        
        // Add styles inline
        svgString = svgString.replace('<svg', `<svg xmlns="http://www.w3.org/2000/svg"`);
        
        const blob = new Blob([svgString], { type: "image/svg+xml" });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement("a");
        link.href = url;
        link.download = "mno-dag-visualization.svg";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    setupEventListeners() {
        // Layout selector
        document.getElementById("layout").addEventListener("change", (e) => {
            this.setLayout(e.target.value);
        });
        
        // Filter selector
        document.getElementById("filter").addEventListener("change", (e) => {
            this.filterByStatus(e.target.value);
        });
        
        // Reset zoom button
        document.getElementById("resetZoom").addEventListener("click", () => {
            this.resetZoom();
        });
        
        // Export SVG button
        document.getElementById("exportSVG").addEventListener("click", () => {
            this.exportSVG();
        });
        
        // Window resize
        window.addEventListener("resize", () => {
            this.width = this.container.node().getBoundingClientRect().width || 800;
            this.svg.attr("width", this.width);
            this.render();
        });
    }
}

// Initialize visualization when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    window.dagViz = new DAGVisualization("#dag-graph");
});