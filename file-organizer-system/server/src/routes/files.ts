/**
 * @GL-governed
 * @GL-layer: server
 * @GL-semantic: files-route
 * @GL-audit-trail: ../.governance/GL_SEMANTIC_ANCHOR.json
 * 
 * GL Unified Charter Activated - Files API Routes
 */

import { Router } from 'express';
import { DatabaseService } from '../services/database';
import { File } from '../types';

const router = Router();
const dbService = new DatabaseService();

/**
 * GET /api/files - Get all files
 */
router.get('/', async (req, res) => {
  try {
    const files = await dbService.getFiles();
    res.json(files);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve files' });
  }
});

/**
 * GET /api/files/:id - Get a specific file
 */
router.get('/:id', async (req, res) => {
  try {
    const files = await dbService.getFiles();
    const file = files.find(f => f.id === req.params.id);

    if (!file) {
      return res.status(404).json({ error: 'File not found' });
    }

    res.json(file);
  } catch (error) {
    res.status(500).json({ error: 'Failed to retrieve file' });
  }
});

/**
 * POST /api/files - Add a new file
 */
router.post('/', async (req, res) => {
  try {
    const fileData: File = req.body;
    const files = await dbService.getFiles();
    files.push(fileData);
    await dbService.saveFiles(files);
    
    res.status(201).json(fileData);
  } catch (error) {
    res.status(500).json({ error: 'Failed to add file' });
  }
});

/**
 * DELETE /api/files/:id - Delete a file
 */
router.delete('/:id', async (req, res) => {
  try {
    const files = await dbService.getFiles();
    const filteredFiles = files.filter(f => f.id !== req.params.id);
    await dbService.saveFiles(filteredFiles);
    
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: 'Failed to delete file' });
  }
});

export default router;